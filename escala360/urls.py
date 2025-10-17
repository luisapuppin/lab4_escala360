# escala360/urls.py
from django.urls import path
from . import views

app_name = 'escala360'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profissionais/', views.lista_profissionais, name='lista_profissionais'),
    path('escalas/', views.visualizar_escalas, name='visualizar_escalas'),
    path('escalas/cadastrar/', views.cadastrar_escala, name='cadastrar_escala'),
    path('substituicoes/pendentes/', views.substituicoes_pendentes, name='substituicoes_pendentes'),
    path('profissionais/carga-excedida/', views.profissionais_carga_horaria_excedida, name='profissionais_carga_excedida'),
    path('substituicoes/solicitar/', views.solicitar_substituicao, name='solicitar_substituicao'),
    path('buscar-profissionais/', views.buscar_profissionais, name='buscar_profissionais'),
    path('buscar-profissionais-disponiveis/', views.buscar_profissionais_disponiveis, name='buscar_profissionais_disponiveis'),
    path('buscar-escalas/<int:profissional_id>/', views.buscar_escalas_profissional, name='buscar_escalas_profissional'),
]
