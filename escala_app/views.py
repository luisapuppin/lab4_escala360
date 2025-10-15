from django.shortcuts import render

# Create your views here.

from django.http import HttpRequest, HttpResponse

# =========================================================
# VIEWS DE LOGIN
# =========================================================


def login_page(request: HttpRequest) -> HttpResponse:
    """
    Renderiza a página de login do Escala360.
    Por enquanto, é apenas um template estático (sem backend de autenticação).
    """
    # O template deve estar salvo em: seu_app/templates/login_template.html
    return render(request, 'login.html')

# =========================================================
# VIEWS DO GESTOR
# =========================================================

def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Renderiza a página inicial do Dashboard do Gestor.
    Rota: /
    Template: gestor_dashboard.html
    """
    # Em um projeto Django real, adicionaríamos aqui a lógica de Contexto (context = {...})
    # para passar dados ao template.
    return render(request, 'home_gestor_v1.html')

def central_aprovacoes(request: HttpRequest) -> HttpResponse:
    """
    Renderiza a Central de Aprovações, onde o gestor processa solicitações.
    Rota: /aprovacoes
    Template: central_aprovacoes.html
    """
    return render(request, 'central_aprovacoes.html')

def escala_consolidada(request: HttpRequest) -> HttpResponse:
    """
    Renderiza a Escala Consolidada, mostrando a cobertura de plantões.
    Rota: /escala
    Template: escala_consolidada.html
    """
    return render(request, 'escala_consolidada.html')

# =========================================================
# VIEWS DO PROFISSIONAL
# =========================================================

def minha_escala(request: HttpRequest) -> HttpResponse:
    """
    Renderiza a escala individual do profissional logado.
    Rota: /minha-escala
    Template: profissional_minha_escala.html
    """
    # Lógica: O profissional seria identificado via request.user (autenticação).
    return render(request, 'home_usuario.html')

def solicitar_substituicao(request: HttpRequest) -> HttpResponse:
    """
    Renderiza a tela para o profissional solicitar a troca ou substituição de um plantão.
    Rota: /solicitar-substituicao
    Template: solicitar_substituicao.html
    """
    # Lógica: Se for um método POST, processaria o formulário de solicitação.
    return render(request, 'solicitar_substituicao.html')

# Nota: Em um projeto Django real, estas funções seriam importadas em 'urls.py'
# para mapear as rotas (paths) do projeto.
