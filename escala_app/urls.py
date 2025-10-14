from django.urls import path
from . import views

# O nome do app é necessário para referenciar as rotas nos templates
app_name = 'escala_app' 

urlpatterns = [
    # Rota principal para o seu dashboard.
    # Ex: Acessada via /escala/
    path('', views.escala_dashboard, name='dashboard'),
]
