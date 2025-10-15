"""
admin.py
Configura e registra os modelos para o Painel Administrativo do Django,
permitindo o gerenciamento de dados (CRUD) via interface web.
"""

from django.contrib import admin

# Register your models here.

from .models import (
    Funcao,
    Local,
    Profissional,
    Plantao,
    Escala,
    Substituicao,
    Auditoria
)


# =========================================================
# Configurações de Modelos Auxiliares (Inline e Simples)
# =========================================================

@admin.register(Funcao)
class FuncaoAdmin(admin.ModelAdmin):
    # Lista os campos na visualização de lista
    list_display = ('id', 'nome')
    # Adiciona campo de busca
    search_fields = ('nome',)

@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

# =========================================================
# Configurações de Modelos Principais
# =========================================================

@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'get_cargo_display', 'email', 'telefone', 'ativo')
    # Filtro lateral para buscar por status de atividade e cargo
    list_filter = ('ativo', 'cargo')
    search_fields = ('nome', 'email', 'cargo')
    # Campos que podem ser editados diretamente na lista
    list_editable = ('ativo',)

@admin.register(Plantao)
class PlantaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'data', 'hora_inicio', 'hora_fim', 'funcao', 'local')
    list_filter = ('data', 'local', 'funcao')
    date_hierarchy = 'data' # Adiciona navegação por data

@admin.register(Escala)
class EscalaAdmin(admin.ModelAdmin):
    list_display = ('plantao_info', 'profissional', 'get_status_display', 'data_alocacao')
    list_filter = ('status', 'profissional__cargo', 'plantao__local')
    search_fields = ('profissional__nome', 'plantao__local__nome')

    # Campo personalizado para mostrar informações relevantes do plantão
    def plantao_info(self, obj):
        return f"{obj.plantao.data.strftime('%d/%m')} - {obj.plantao.local.nome} ({obj.plantao.funcao.nome})"
    plantao_info.short_description = "Plantão (Data - Local - Função)"


@admin.register(Substituicao)
class SubstituicaoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'escala_original',
        'profissional_solicitante',
        'profissional_substituto',
        'get_status_display',
        'data_solicitacao'
    )
    list_filter = ('status', 'data_solicitacao', 'profissional_solicitante__cargo')
    search_fields = (
        'profissional_solicitante__nome',
        'profissional_substituto__nome',
    )
    # Define campos somente-leitura após a criação
    readonly_fields = ('data_solicitacao',)


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    # Opcionalmente, pode ser apenas leitura, pois são registros de histórico
    readonly_fields = ('entidade', 'id_entidade', 'acao', 'usuario', 'data_hora')
    list_display = ('id', 'get_entidade_display', 'id_entidade', 'get_acao_display', 'usuario', 'data_hora')
    list_filter = ('entidade', 'acao', 'usuario')
    search_fields = ('usuario', 'entidade', 'acao')
    ordering = ('-data_hora',)
