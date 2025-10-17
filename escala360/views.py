from django.shortcuts import render

# Create your views here.

# escala360/views.py
from django.db.models import Q, Sum, F
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Profissional, Plantao, Escala, Substituicao, Auditoria, Funcao, Local
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .forms import EscalaForm, PlantaoForm
from django.contrib.messages import get_messages

def dashboard(request):
    """Dashboard principal do sistema"""
    # Estatísticas básicas
    total_profissionais = Profissional.objects.filter(ativo=True).count()
    total_plantoes = Plantao.objects.count()
    escalas_ativas = Escala.objects.filter(status='ativo').count()
    substituicoes_pendentes = Substituicao.objects.filter(status='pendente').count()
    
    # Próximos plantões (próximos 7 dias) - com select_related para carregar funcao e local
    data_inicio = timezone.now().date()
    data_fim = data_inicio + timedelta(days=7)
    proximos_plantoes = Plantao.objects.filter(
        data__range=[data_inicio, data_fim]
    ).select_related('funcao', 'local').order_by('data', 'hora_inicio')[:10]
    
    context = {
        'total_profissionais': total_profissionais,
        'total_plantoes': total_plantoes,
        'escalas_ativas': escalas_ativas,
        'substituicoes_pendentes': substituicoes_pendentes,
        'proximos_plantoes': proximos_plantoes,
    }
    return render(request, 'escala360/dashboard.html', context)

def lista_profissionais(request):
    """Lista de profissionais com informações de carga horária"""
    profissionais = Profissional.objects.filter(ativo=True)
    
    # Calcular carga horária semanal para cada profissional
    for profissional in profissionais:
        # Esta é uma simplificação - em produção, calcularíamos baseado nas escalas da semana
        profissional.carga_horaria_semanal = 40  # Valor padrão
    
    context = {
        'profissionais': profissionais,
    }
    return render(request, 'escala360/lista_profissionais.html', context)

def visualizar_escalas(request):
    """Visualização consolidada das escalas considerando substituições"""
    # Buscar escalas ativas ordenadas por data e horário
    escalas = Escala.objects.select_related('id_plantao', 'id_profissional')\
                          .filter(status='ativo')\
                          .order_by('id_plantao__data', 'id_plantao__hora_inicio')
    
    # Buscar todas as substituições aprovadas e pendentes
    substituicoes_aprovadas = Substituicao.objects.filter(
        status='aprovado'
    ).select_related(
        'id_escala_original__id_plantao',
        'id_escala_original__id_profissional',
        'id_profissional_substituto'
    )
    
    substituicoes_pendentes = Substituicao.objects.filter(
        status='pendente'
    ).select_related(
        'id_escala_original__id_plantao',
        'id_escala_original__id_profissional',
        'id_profissional_substituto'
    )
    
    # Criar dicionários para acesso rápido
    substituicoes_aprovadas_dict = {}
    for subst in substituicoes_aprovadas:
        substituicoes_aprovadas_dict[subst.id_escala_original_id] = subst
    
    substituicoes_pendentes_dict = {}
    for subst in substituicoes_pendentes:
        substituicoes_pendentes_dict[subst.id_escala_original_id] = subst
    
    # Processar escalas para incluir informações de substituição
    escalas_processadas = []
    for escala in escalas:
        escala_data = {
            'id': escala.id,
            'id_plantao': escala.id_plantao,
            'id_profissional': escala.id_profissional,
            'status': escala.status,
            'data_alocacao': escala.data_alocacao,
            'substituicao_aprovada': False,
            'substituicao_pendente': False,
            'profissional_atual': escala.id_profissional,  # Inicialmente o profissional original
            'substituicao_info': None
        }
        
        # Verificar se há substituição aprovada para esta escala
        if escala.id in substituicoes_aprovadas_dict:
            subst = substituicoes_aprovadas_dict[escala.id]
            escala_data['substituicao_aprovada'] = True
            escala_data['profissional_atual'] = subst.id_profissional_substituto
            escala_data['substituicao_info'] = subst
        
        # Verificar se há substituição pendente para esta escala
        elif escala.id in substituicoes_pendentes_dict:
            subst = substituicoes_pendentes_dict[escala.id]
            escala_data['substituicao_pendente'] = True
            escala_data['profissional_atual'] = subst.id_profissional_substituto
            escala_data['substituicao_info'] = subst
        
        escalas_processadas.append(escala_data)
    
    # Agrupar por data para facilitar a visualização
    escalas_por_data = {}
    for escala_data in escalas_processadas:
        data = escala_data['id_plantao'].data
        if data not in escalas_por_data:
            escalas_por_data[data] = []
        escalas_por_data[data].append(escala_data)
    
    # Ordenar o dicionário por data (chaves)
    escalas_por_data_ordenado = dict(sorted(escalas_por_data.items()))
    
    context = {
        'escalas_por_data': escalas_por_data_ordenado,
    }
    return render(request, 'escala360/visualizar_escalas.html', context)

def substituicoes_pendentes(request):
    """Lista de substituições pendentes de aprovação"""
    # Buscar todas as substituições ordenadas pela data do plantão (mais antiga primeiro)
    substituicoes = Substituicao.objects.select_related(
        'id_escala_original__id_plantao__local',
        'id_profissional_solicitante',
        'id_profissional_substituto'
    ).order_by('id_escala_original__id_plantao__data', 'id_escala_original__id_plantao__hora_inicio')
    
    context = {
        'substituicoes': substituicoes,
    }
    return render(request, 'escala360/substituicoes_pendentes.html', context)

def profissionais_carga_horaria_excedida(request):
    """Lista profissionais que atingiram ou ultrapassaram carga horária semanal"""
    
    # Obter data de referência do request ou usar a data atual
    data_referencia_str = request.GET.get('data_referencia')
    if data_referencia_str:
        try:
            data_referencia = datetime.strptime(data_referencia_str, '%Y-%m-%d').date()
        except ValueError:
            data_referencia = timezone.now().date()
    else:
        data_referencia = timezone.now().date()
    
    # Calcular início da semana (segunda-feira) da data de referência
    inicio_semana = data_referencia - timedelta(days=data_referencia.weekday())
    fim_semana = inicio_semana + timedelta(days=6)
    
    # Buscar profissionais ativos
    profissionais = Profissional.objects.filter(ativo=True)
    
    profissionais_com_carga = []
    
    for profissional in profissionais:
        # Calcular horas trabalhadas na semana da data de referência
        horas_trabalhadas = profissional.horas_trabalhadas_semana(data_referencia)
        plantoes_semana = []
        
        # Buscar plantões da semana para detalhamento
        escalas_semana = Escala.objects.filter(
            id_profissional=profissional,
            id_plantao__data__range=[inicio_semana, fim_semana],
            status='ativo'
        ).select_related('id_plantao')
        
        for escala in escalas_semana:
            plantao = escala.id_plantao
            # Calcular horas do plantão
            inicio = datetime.combine(plantao.data, plantao.hora_inicio)
            fim = datetime.combine(plantao.data, plantao.hora_fim)
            horas_plantao = (fim - inicio).seconds / 3600
            
            plantoes_semana.append({
                'data': plantao.data,
                'horario': f"{plantao.hora_inicio} - {plantao.hora_fim}",
                'horas': round(horas_plantao, 2)
            })
        
        # Verificar se excedeu a carga horária
        carga_maxima = profissional.carga_horaria_maxima_semanal
        excedeu = horas_trabalhadas >= carga_maxima
        percentual = (horas_trabalhadas / carga_maxima * 100) if carga_maxima > 0 else 0
        
        if excedeu:
            profissionais_com_carga.append({
                'profissional': profissional,
                'horas_trabalhadas': round(horas_trabalhadas, 2),
                'carga_maxima': carga_maxima,
                'percentual': round(percentual, 1),
                'plantoes_semana': plantoes_semana,
                'diferenca': round(horas_trabalhadas - carga_maxima, 2)
            })
    
    # Ordenar por maior excedente
    profissionais_com_carga.sort(key=lambda x: x['diferenca'], reverse=True)
    
    context = {
        'profissionais_excedidos': profissionais_com_carga,
        'periodo_semana': f"{inicio_semana} a {fim_semana}",
        'total_excedidos': len(profissionais_com_carga),
        'data_selecionada': data_referencia,
        'semana_atual': data_referencia == timezone.now().date(),
    }
    
    return render(request, 'escala360/profissionais_carga_excedida.html', context)

## Cadastrar solicitação

def sugerir_substitutos(escala_original):
    """Sugere 3 substitutos disponíveis com menor carga horária"""
    plantao = escala_original.id_plantao
    profissional_original = escala_original.id_profissional
    
    # Buscar profissionais com mesma função e que estão ativos
    profissionais_compatíveis = Profissional.objects.filter(
        ativo=True,
        cargo=profissional_original.cargo  # Assumindo mesma função = mesmo cargo
    ).exclude(id=profissional_original.id)
    
    sugestoes = []
    
    for profissional in profissionais_compatíveis:
        # Verificar disponibilidade no horário
        if not verificar_conflito_horario(profissional, plantao):
            # Calcular carga horária semanal
            horas_trabalhadas = profissional.horas_trabalhadas_semana()
            carga_maxima = profissional.carga_horaria_maxima_semanal
            percentual_utilizado = (horas_trabalhadas / carga_maxima * 100) if carga_maxima > 0 else 0
            
            sugestoes.append({
                'profissional': profissional,
                'horas_trabalhadas': horas_trabalhadas,
                'carga_maxima': carga_maxima,
                'percentual_utilizado': percentual_utilizado,
                'disponivel': True
            })
    
    # Ordenar por menor carga horária (menos ocupados primeiro)
    sugestoes.sort(key=lambda x: x['horas_trabalhadas'])
    
    # Retornar apenas os 3 primeiros
    return sugestoes[:3]

def solicitar_substituicao(request):
    """View para solicitar uma substituição usando seletores"""
    # Buscar dados para os seletores
    profissionais = Profissional.objects.filter(ativo=True).order_by('nome')
    
    # Buscar escalas futuras (próximos 30 dias)
    data_inicio = timezone.now().date()
    data_fim = data_inicio + timedelta(days=30)
    escalas_futuras = Escala.objects.filter(
        id_plantao__data__range=[data_inicio, data_fim],
        status='ativo'
    ).select_related('id_plantao', 'id_profissional').order_by('id_plantao__data')
    
    sugestoes = []
    escala_selecionada = None
    
    if request.method == 'POST':
        try:
            id_escala_original = request.POST.get('id_escala_original')
            id_profissional_substituto = request.POST.get('id_profissional_substituto')
            
            if not id_escala_original or not id_profissional_substituto:
                messages.error(request, 'Por favor, selecione todos os campos obrigatórios.')
                return render(request, 'escala360/solicitar_substituicao.html', {
                    'profissionais': profissionais,
                    'escalas_futuras': escalas_futuras,
                    'sugestoes': sugestoes
                })
            
            escala_original = Escala.objects.get(id=id_escala_original)
            profissional_substituto = Profissional.objects.get(id=id_profissional_substituto)
            profissional_solicitante = escala_original.id_profissional
            
            # Verificar se não está tentando substituir por si mesmo
            if profissional_solicitante.id == profissional_substituto.id:
                messages.error(request, 'Não é possível solicitar substituição para si mesmo.')
                return render(request, 'escala360/solicitar_substituicao.html', {
                    'profissionais': profissionais,
                    'escalas_futuras': escalas_futuras,
                    'sugestoes': sugestoes
                })
            
            # Verificar conflito de horário
            if verificar_conflito_horario(profissional_substituto, escala_original.id_plantao):
                messages.error(request, 'O profissional substituto já tem um plantão no mesmo horário!')
                return render(request, 'escala360/solicitar_substituicao.html', {
                    'profissionais': profissionais,
                    'escalas_futuras': escalas_futuras,
                    'sugestoes': sugestoes
                })
            
            # Verificar antecedência mínima (12 horas)
            plantao = escala_original.id_plantao
            horas_antecedencia = (plantao.data - timezone.now().date()).days * 24
            
            if horas_antecedencia < 12:
                messages.warning(request, 'Substituição solicitada com menos de 12h de antecedência. Será necessária aprovação do supervisor.')
            
            # Criar substituição
            substituicao = Substituicao.objects.create(
                id_escala_original=escala_original,
                id_profissional_solicitante=profissional_solicitante,
                id_profissional_substituto=profissional_substituto,
                status='pendente'
            )
            
            # Registrar auditoria
            Auditoria.objects.create(
                entidade='substituicao',
                id_entidade=substituicao.id,
                acao='solicitado',
                usuario=request.user.username if request.user.is_authenticated else 'sistema'
            )
            
            messages.success(request, 'Substituição solicitada com sucesso! Aguarde aprovação.')
            return redirect('escala360:substituicoes_pendentes')
            
        except (Escala.DoesNotExist, Profissional.DoesNotExist) as e:
            messages.error(request, 'Erro ao processar a solicitação. Verifique os dados selecionados.')
    
    # Se foi selecionada uma escala via GET (para mostrar sugestões)
    escala_id = request.GET.get('escala_id')
    if escala_id:
        try:
            escala_selecionada = Escala.objects.get(id=escala_id)
            sugestoes = sugerir_substitutos(escala_selecionada)
        except Escala.DoesNotExist:
            pass
    
    return render(request, 'escala360/solicitar_substituicao.html', {
        'profissionais': profissionais,
        'escalas_futuras': escalas_futuras,
        'sugestoes': sugestoes,
        'escala_selecionada': escala_selecionada
    })

def cadastrar_escala(request):
    """View para cadastrar nova escala"""
    # Limpar mensagens antigas se for um GET request
    if request.method == 'GET':
        storage = get_messages(request)
        for message in storage:
            pass  # Isso limpa as mensagens
    
    # Buscar dados para os seletores
    profissionais = Profissional.objects.filter(ativo=True).order_by('nome')
    funcoes = Funcao.objects.all()
    locais = Local.objects.filter(ativo=True)
    
    if request.method == 'POST':
        form_plantao = PlantaoForm(request.POST, prefix='plantao')
        form_escala = EscalaForm(request.POST, prefix='escala')
        
        if form_plantao.is_valid() and form_escala.is_valid():
            try:
                # Salvar o plantão primeiro
                plantao = form_plantao.save()
                
                # Associar o plantão à escala
                escala = form_escala.save(commit=False)
                escala.id_plantao = plantao
                
                # Verificar conflito de horário
                if verificar_conflito_horario(escala.id_profissional, plantao):
                    messages.error(request, 'Este profissional já tem um plantão no mesmo horário!')
                    # Deletar o plantão criado
                    plantao.delete()
                    return render(request, 'escala360/cadastrar_escala.html', {
                        'form_plantao': form_plantao,
                        'form_escala': form_escala,
                        'profissionais': profissionais,
                        'funcoes': funcoes,
                        'locais': locais
                    })
                
                # Verificar carga horária semanal
                if verificar_carga_horaria_excedida(escala.id_profissional, plantao):
                    messages.warning(request, 'Atenção: Este profissional pode exceder a carga horária semanal com este plantão.')
                
                escala.save()
                
                # Registrar auditoria
                Auditoria.objects.create(
                    entidade='escala',
                    id_entidade=escala.id,
                    acao='criado',
                    usuario=request.user.username if request.user.is_authenticated else 'sistema'
                )
                
                messages.success(request, 'Escala cadastrada com sucesso!')
                return redirect('escala360:cadastrar_escala')  # Redireciona para a mesma página para limpar o form
                
            except Exception as e:
                messages.error(request, f'Erro ao salvar escala: {str(e)}')
        else:
            # Mostrar erros de validação
            if form_escala.errors:
                for field, errors in form_escala.errors.items():
                    for error in errors:
                        messages.error(request, f'Erro no campo {field}: {error}')
    else:
        form_plantao = PlantaoForm(prefix='plantao')
        form_escala = EscalaForm(prefix='escala')
    
    return render(request, 'escala360/cadastrar_escala.html', {
        'form_plantao': form_plantao,
        'form_escala': form_escala,
        'profissionais': profissionais,
        'funcoes': funcoes,
        'locais': locais
    })

def verificar_carga_horaria_excedida(profissional, novo_plantao):
    """Verifica se o profissional vai exceder a carga horária semanal"""
    # Calcular horas trabalhadas na SEMANA do novo plantão
    horas_trabalhadas = profissional.horas_trabalhadas_semana(novo_plantao.data)
    
    # Calcular horas do novo plantão
    from datetime import datetime
    inicio_novo = datetime.combine(novo_plantao.data, novo_plantao.hora_inicio)
    fim_novo = datetime.combine(novo_plantao.data, novo_plantao.hora_fim)
    horas_novo_plantao = (fim_novo - inicio_novo).seconds / 3600
    
    horas_totais = horas_trabalhadas + horas_novo_plantao
    
    print(f"DEBUG Carga horária: {profissional.nome} - Atual: {horas_trabalhadas}h + Novo: {horas_novo_plantao}h = Total: {horas_totais}h / Máximo: {profissional.carga_horaria_maxima_semanal}h")
    
    return horas_totais > profissional.carga_horaria_maxima_semanal

def buscar_profissionais_disponiveis(request):
    """API para buscar profissionais disponíveis em um determinado horário"""
    data = request.GET.get('data')
    hora_inicio = request.GET.get('hora_inicio')
    hora_fim = request.GET.get('hora_fim')
    funcao_id = request.GET.get('funcao_id')
    
    print(f"DEBUG: Buscando profissionais - data: {data}, inicio: {hora_inicio}, fim: {hora_fim}")
    
    if not all([data, hora_inicio, hora_fim]):
        return JsonResponse([], safe=False)
    
    try:
        from datetime import datetime
        data_obj = datetime.strptime(data, '%Y-%m-%d').date()
        hora_inicio_obj = datetime.strptime(hora_inicio, '%H:%M').time()
        hora_fim_obj = datetime.strptime(hora_fim, '%H:%M').time()
        
        # Buscar profissionais ativos
        profissionais = Profissional.objects.filter(ativo=True)
        
        if funcao_id:
            # Filtrar por função específica se fornecida
            try:
                funcao = Funcao.objects.get(id=funcao_id)
                # Buscar profissionais com cargo similar à função
                profissionais = profissionais.filter(cargo__icontains=funcao.nome.split()[0])
            except Funcao.DoesNotExist:
                pass
        
        profissionais_disponiveis = []
        
        for profissional in profissionais:
            # Calcular horas trabalhadas na SEMANA da data selecionada
            horas_trabalhadas = profissional.horas_trabalhadas_semana(data_obj)
            print(f"DEBUG: {profissional.nome} - {horas_trabalhadas}h (na semana de {data_obj})")
            
            # Verificar conflitos de horário
            conflitos = Escala.objects.filter(
                id_profissional=profissional,
                id_plantao__data=data_obj,
                status='ativo'
            ).select_related('id_plantao')
            
            disponivel = True
            for escala in conflitos:
                plantao_existente = escala.id_plantao
                if (plantao_existente.hora_inicio < hora_fim_obj and 
                    plantao_existente.hora_fim > hora_inicio_obj):
                    disponivel = False
                    break
            
            if disponivel:
                carga_maxima = profissional.carga_horaria_maxima_semanal
                percentual = (horas_trabalhadas / carga_maxima * 100) if carga_maxima > 0 else 0
                
                profissionais_disponiveis.append({
                    'id': profissional.id,
                    'nome': profissional.nome,
                    'cargo': profissional.cargo,
                    'email': profissional.email,
                    'horas_trabalhadas': horas_trabalhadas,
                    'carga_maxima': carga_maxima,
                    'percentual': round(percentual, 1),
                    'disponivel': True
                })
        
        # Ordenar por menor carga horária
        profissionais_disponiveis.sort(key=lambda x: x['horas_trabalhadas'])
        
        print(f"DEBUG: Retornando {len(profissionais_disponiveis)} profissionais")
        return JsonResponse(profissionais_disponiveis, safe=False)
        
    except ValueError as e:
        print(f"Erro ao processar dados: {e}")
        return JsonResponse([], safe=False)
    
def verificar_conflito_horario(profissional, plantao_alvo):
    """Verifica se o profissional já tem plantão no mesmo horário"""
    conflitos = Escala.objects.filter(
        id_profissional=profissional,
        id_plantao__data=plantao_alvo.data,
        status='ativo'
    ).exclude(id_plantao=plantao_alvo)
    
    for escala in conflitos:
        plantao_existente = escala.id_plantao
        # Verificar sobreposição de horários
        if (plantao_existente.hora_inicio < plantao_alvo.hora_fim and 
            plantao_existente.hora_fim > plantao_alvo.hora_inicio):
            return True
    
    return False

def buscar_profissionais(request):
    """API para buscar profissionais (autocomplete)"""
    query = request.GET.get('q', '')
    cargo_filter = request.GET.get('cargo', '')
    
    profissionais = Profissional.objects.filter(ativo=True)
    
    if query:
        profissionais = profissionais.filter(
            Q(nome__icontains=query) | Q(email__icontains=query)
        )
    
    if cargo_filter:
        profissionais = profissionais.filter(cargo__icontains=cargo_filter)
    
    # Limitar a 10 resultados
    profissionais = profissionais[:10]
    
    results = []
    for prof in profissionais:
        results.append({
            'id': prof.id,
            'nome': prof.nome,
            'cargo': prof.cargo,
            'email': prof.email,
            'horas_semana': prof.horas_trabalhadas_semana(),
            'carga_maxima': prof.carga_horaria_maxima_semanal
        })
    
    return JsonResponse(results, safe=False)

def buscar_escalas_profissional(request, profissional_id):
    """API para buscar escalas de um profissional"""
    profissional = get_object_or_404(Profissional, id=profissional_id)
    
    # Buscar escalas futuras do profissional
    from django.utils import timezone
    escalas = Escala.objects.filter(
        id_profissional=profissional,
        id_plantao__data__gte=timezone.now().date(),
        status='ativo'
    ).select_related('id_plantao').order_by('id_plantao__data', 'id_plantao__hora_inicio')
    
    results = []
    for escala in escalas:
        plantao = escala.id_plantao
        results.append({
            'id': escala.id,
            'data': plantao.data.strftime('%d/%m/%Y'),
            'horario': f"{plantao.hora_inicio} - {plantao.hora_fim}",
            'funcao': plantao.id_funcao,
            'local': plantao.id_local
        })
    
    return JsonResponse(results, safe=False)

def aprovar_substituicao(request, substituicao_id):
    """View para aprovar uma substituição"""
    if request.method == 'POST':
        substituicao = get_object_or_404(Substituicao, id=substituicao_id)
        
        # Verificar se a substituição ainda está pendente
        if substituicao.status != 'pendente':
            messages.error(request, 'Esta substituição já foi processada.')
            return redirect('escala360:substituicoes_pendentes')
        
        # Verificar conflitos de horário do substituto
        plantao_original = substituicao.id_escala_original.id_plantao
        if verificar_conflito_horario(substituicao.id_profissional_substituto, plantao_original):
            messages.error(request, f'O profissional {substituicao.id_profissional_substituto.nome} já tem um plantão no mesmo horário!')
            return redirect('escala360:substituicoes_pendentes')
        
        # Verificar carga horária do substituto
        if verificar_carga_horaria_excedida(substituicao.id_profissional_substituto, plantao_original):
            messages.warning(request, f'Atenção: O profissional {substituicao.id_profissional_substituto.nome} pode exceder a carga horária semanal.')
        
        # Aprovar a substituição
        substituicao.status = 'aprovado'
        substituicao.save()
        
        # Registrar auditoria
        Auditoria.objects.create(
            entidade='substituicao',
            id_entidade=substituicao.id,
            acao='aprovado',
            usuario=request.user.username if request.user.is_authenticated else 'supervisor'
        )
        
        messages.success(request, f'Substituição aprovada com sucesso! {substituicao.id_profissional_solicitante.nome} → {substituicao.id_profissional_substituto.nome}')
    
    return redirect('escala360:substituicoes_pendentes')

def rejeitar_substituicao(request, substituicao_id):
    """View para rejeitar uma substituição"""
    if request.method == 'POST':
        substituicao = get_object_or_404(Substituicao, id=substituicao_id)
        
        # Verificar se a substituição ainda está pendente
        if substituicao.status != 'pendente':
            messages.error(request, 'Esta substituição já foi processada.')
            return redirect('escala360:substituicoes_pendentes')
        
        # Rejeitar a substituição
        substituicao.status = 'rejeitado'
        substituicao.save()
        
        # Registrar auditoria
        Auditoria.objects.create(
            entidade='substituicao',
            id_entidade=substituicao.id,
            acao='rejeitado',
            usuario=request.user.username if request.user.is_authenticated else 'supervisor'
        )
        
        messages.success(request, f'Substituição rejeitada. {substituicao.id_profissional_solicitante.nome} permanece no plantão.')
    
    return redirect('escala360:substituicoes_pendentes')

