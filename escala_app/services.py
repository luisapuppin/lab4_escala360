from datetime import timedelta, datetime, time
from django.db.models import Sum, Q, F, ExpressionWrapper, DurationField
from django.utils import timezone # Usado para consultas de tempo real
from .models import Profissional, Escala, Plantao, Substituicao

# === LÓGICA DE NEGÓCIO: SUGESTÃO DE SUBSTITUTOS ===

def sugerir_substitutos(plantao_id: int):
    """
    Implementa a Regra de Negócio 4: Sugerir 3 substitutos disponíveis 
    com a menor carga horária acumulada na semana.
    """
    try:
        # 1. Recupera o Plantão que precisa de substituição
        plantao_original = Plantao.objects.get(pk=plantao_id)
    except Plantao.DoesNotExist:
        print(f"ERRO: Plantão com ID {plantao_id} não encontrado.")
        return []

    # 2. Define o período da semana para cálculo de carga horária
    # (Simples: 7 dias a partir da data do plantão)
    # ATENÇÃO: date.weekday() retorna 0 para segunda, 6 para domingo.
    data_inicio_semana = plantao_original.data - timedelta(days=plantao_original.data.weekday())
    data_fim_semana = data_inicio_semana + timedelta(days=6)

    # 3. Identifica profissionais alocados no MESMO horário/função/local.
    conflito_q = Escala.objects.filter(
        plantao__data=plantao_original.data,
        plantao__hora_inicio__lte=plantao_original.hora_fim, 
        plantao__hora_fim__gte=plantao_original.hora_inicio,
        plantao__id_funcao=plantao_original.id_funcao,
        plantao__id_local=plantao_original.id_local,
        status='ativo'
    ).values_list('profissional_id', flat=True)

    # 4. Calcula a carga horária acumulada dos profissionais ativos e filtra os alocados em conflito
    
    # Define a expressão de duração do plantão como (hora_fim - hora_inicio)
    plantao_duration_expression = ExpressionWrapper(
        F('escalas__plantao__hora_fim') - F('escalas__plantao__hora_inicio'),
        output_field=DurationField()
    )

    profissionais_com_carga = Profissional.objects.filter(
        ativo=True
    ).exclude(
        id__in=conflito_q
    ).annotate(
        # CORREÇÃO: Usamos o ExpressionWrapper para calcular a duração e depois somamos
        carga_acumulada_segundos=Sum(
            plantao_duration_expression,
            filter=Q(
                escalas__plantao__data__gte=data_inicio_semana,
                escalas__plantao__data__lte=data_fim_semana,
                escalas__status='ativo'
            )
        )
    ).order_by('carga_acumulada_segundos')[:3]

    # 5. Formata o resultado
    sugestoes = []
    for p in profissionais_com_carga:
        carga_timedelta = p.carga_acumulada_segundos
        
        if carga_timedelta is None:
            carga_segundos = 0
        elif isinstance(carga_timedelta, timedelta):
            carga_segundos = carga_timedelta.total_seconds()
        else:
            carga_segundos = float(carga_timedelta)

        carga_horas = int(carga_segundos // 3600)
        carga_minutos = int((carga_segundos % 3600) // 60)
        
        sugestoes.append({
            'id': p.id,
            'nome': p.nome,
            'cargo': p.cargo,
            'carga_semanal_acumulada': f"{carga_horas:02d}:{carga_minutos:02d}h"
        })
        
    return sugestoes


# === INSTRUÇÕES PARA CONSULTAS SQL ===

def listar_profissionais_com_carga_excedida():
    """
    1. Listar profissionais que já atingiram ou ultrapassaram sua carga horária semanal.
    (Regra de Negócio 1)
    """
    # Define a expressão de duração do plantão como (hora_fim - hora_inicio)
    plantao_duration_expression = ExpressionWrapper(
        F('escalas__plantao__hora_fim') - F('escalas__plantao__hora_inicio'),
        output_field=DurationField()
    )

    # Define o início da semana atual (domingo ou segunda, dependendo da configuração local, 
    # mas usando Monday=0 para garantir a lógica)
    hoje = datetime.now().date()
    data_inicio_semana = hoje - timedelta(days=hoje.weekday())

    # 1. Anota a carga horária acumulada na semana (em segundos)
    # 2. Filtra aqueles cuja carga acumulada é maior que a carga máxima semanal do profissional
    # 3. Nota: O campo carga_horaria_maxima_semanal está em horas, então convertemos para segundos (multiplicando por 3600)
    
    profissionais_excedidos = Profissional.objects.filter(ativo=True).annotate(
        carga_acumulada_segundos=Sum(
            plantao_duration_expression,
            filter=Q(
                escalas__plantao__data__gte=data_inicio_semana,
                escalas__status='ativo'
            )
        )
    ).filter(
        # Filtra onde a carga acumulada é maior que a carga máxima semanal * 3600 (segundos)
        carga_acumulada_segundos__gt=F('carga_horaria_maxima_semanal') * 3600
    ).order_by('carga_acumulada_segundos')

    resultados = []
    for p in profissionais_excedidos:
        # Conversão de timedelta para segundos para formatação
        carga_segundos = p.carga_acumulada_segundos.total_seconds()
        carga_horas = int(carga_segundos // 3600)
        carga_minutos = int((carga_segundos % 3600) // 60)
        
        resultados.append({
            'id': p.id,
            'nome': p.nome,
            'cargo': p.cargo,
            'carga_maxima': f"{p.carga_horaria_maxima_semanal}h",
            'carga_atual': f"{carga_horas:02d}:{carga_minutos:02d}h"
        })

    return resultados


def consultar_plantoes_sem_profissional(horas_futuras=48):
    """
    2. Consultar plantões sem profissional alocado nas próximas N horas.
    """
    # Calcula o ponto de corte: agora + N horas
    momento_corte = timezone.now() + timedelta(hours=horas_futuras)
    
    # 1. Encontra Plantões que ocorrem até o momento de corte
    # 2. Exclui os IDs de Plantões que possuem alguma Escala alocada ('ativo')
    
    # IDs de todos os plantões que JÁ TÊM uma escala ativa
    plantoes_alocados_ids = Escala.objects.filter(status='ativo').values_list('plantao_id', flat=True)

    # Consulta os plantões que estão no futuro (data > hoje OU (data = hoje E hora_inicio > agora))
    # E que NÃO estão na lista de IDs alocados
    
    # Combina data e hora_inicio para fazer a comparação com o momento de corte (datetime)
    # No SQLite, não é simples combinar data e time, então simplificamos comparando a data
    # e fazemos a verificação de alocação (sem profissional) de forma direta.
    
    # Para ser mais preciso, filtramos apenas plantões futuros
    plantoes_futuros = Plantao.objects.filter(
        data__gte=timezone.now().date()
    )

    # Filtra os que não possuem um relacionamento de escala ativo (profissional_id não é NULL)
    # NOTA: Como usamos Escala para alocação, buscamos plantões cujo ID não está nas Escalas Ativas.
    plantoes_sem_profissional = plantoes_futuros.exclude(
        id__in=plantoes_alocados_ids
    ).order_by('data', 'hora_inicio')

    resultados = []
    for p in plantoes_sem_profissional:
        # Uma verificação extra para garantir que não estão muito longe no futuro:
        plantao_datetime_inicio = datetime.combine(p.data, p.hora_inicio)
        if plantao_datetime_inicio < momento_corte:
            resultados.append({
                'id': p.id,
                'data': p.data.strftime('%Y-%m-%d'),
                'inicio': p.hora_inicio.strftime('%H:%M'),
                'funcao': p.id_funcao,
                'local': p.id_local,
            })
            
    return resultados


def listar_substituicoes_pendentes():
    """
    3. Listar todas as substituições pendentes de aprovação.
    """
    # Consulta direta na tabela Substituicao, filtrando pelo status 'pendente'
    # Os nomes dos campos são substituicoes_solicitadas e substituicoes_realizadas no modelo Profissional
    
    substituicoes_pendentes = Substituicao.objects.filter(
        status='pendente'
    ).select_related(
        # Pre-busca os objetos relacionados para evitar consultas N+1
        'profissional_substituto', # Nome do campo no model Substituicao (id_profissional_substituto)
        'profissional_solicitante', # Nome do campo no model Substituicao (id_profissional_solicitante)
        'escala_original__plantao' # Acessa o Plantao da Escala original
    ).order_by('data_solicitacao')

    resultados = []
    for s in substituicoes_pendentes:
        plantao_data = s.escala_original.plantao.data.strftime('%Y-%m-%d')
        plantao_hora = s.escala_original.plantao.hora_inicio.strftime('%H:%M')
        
        resultados.append({
            'id': s.id,
            'plantao': f"ID {s.escala_original.plantao.id} em {plantao_data} às {plantao_hora}",
            'solicitante': s.profissional_solicitante.nome,
            'substituto_sugerido': s.profissional_substituto.nome,
            'data_solicitacao': s.data_solicitacao.strftime('%Y-%m-%d %H:%M')
        })
        
    return resultados
