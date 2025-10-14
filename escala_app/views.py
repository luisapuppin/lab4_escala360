from django.shortcuts import render
from .services import (
    sugerir_substitutos,
    listar_profissionais_com_carga_excedida,
    consultar_plantoes_sem_profissional,
    listar_substituicoes_pendentes
)
from datetime import datetime, time

def escala_dashboard(request):
    """
    Simula a execução da lógica de negócios e das consultas SQL,
    enviando os resultados para o template (e logando no terminal).
    """
    
    # 1. Teste da Lógica de Sugestão de Substitutos (Plantão ID 1)
    plantao_teste_id = 1
    sugestoes = sugerir_substitutos(plantao_teste_id)
    
    print("\n--- Resultado: Sugestão de Substitutos ---")
    print(f"Plantão ID {plantao_teste_id} precisa de substituto. Sugestões: {sugestoes}")

    # 2. Teste da Consulta: Profissionais com Carga Excedida
    profissionais_excedidos = listar_profissionais_com_carga_excedida()
    print("\n--- Resultado: Profissionais com Carga Excedida ---")
    print(f"Excedidos: {profissionais_excedidos}")

    # 3. Teste da Consulta: Plantões sem Profissional (próximas 48h)
    plantoes_vagos = consultar_plantoes_sem_profissional(horas_futuras=48)
    print("\n--- Resultado: Plantões sem Profissional (48h) ---")
    print(f"Plantões vagos: {plantoes_vagos}")

    # 4. Teste da Consulta: Substituições Pendentes
    substituicoes_pendentes = listar_substituicoes_pendentes()
    print("\n--- Resultado: Substituições Pendentes ---")
    print(f"Substituições pendentes: {substituicoes_pendentes}")
    
    # CRIAÇÃO DO CONTEXTO (DICIONÁRIO)
    # Todos os resultados das consultas SÃO INCLUÍDOS AQUI para serem 
    # visualizados no template escala_dashboard.html.
    context = {
        'current_date': datetime.now(),
        'sugestoes_substituto': sugestoes,
        'profissionais_excedidos': profissionais_excedidos,
        'plantoes_vagos': plantoes_vagos,
        'substituicoes_pendentes': substituicoes_pendentes,
        # Você pode adicionar variáveis simples, se necessário:
        'plantao_analisado_id': plantao_teste_id 
    }

    # Renderiza o template, enviando o dicionário de contexto
    return render(request, 'escala_app/escala_dashboard.html', context)
