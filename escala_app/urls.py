from django.urls import path
from . import views

app_name = 'escala_app' 

urlpatterns = [
    # =========================================================
    # ROTA DE LOGIN
    # Rota base para acesso ao sistema.
    # =========================================================
    path('', views.login_page, name='login'), # Rota raiz: /

    # =========================================================
    # ROTAS DO GESTOR (Dashboard, Escala Consolidada, Aprovações)
    # A rota raiz (/) será o Dashboard do Gestor, por padrão.
    # =========================================================
    path('home/', views.dashboard, name='dashboard'),  
    path('aprovacoes/', views.central_aprovacoes, name='central_aprovacoes'), # Rota: /aprovacoes
    path('escala/', views.escala_consolidada, name='escala_consolidada'), # Rota: /escala

    # =========================================================
    # ROTAS DO PROFISSIONAL (Minha Escala, Solicitação)
    # Estas rotas são acessíveis ao profissional.
    # =========================================================
    path('minha-escala/', views.minha_escala, name='minha_escala'), # Rota: /minha-escala
    path('solicitar-substituicao/', views.solicitar_substituicao, name='solicitar_substituicao'), # Rota: /solicitar-substituicao
]
