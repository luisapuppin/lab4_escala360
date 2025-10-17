from django.contrib import admin

# Register your models here.

# escala360/admin.py
from django.contrib import admin
from .models import Profissional, Plantao, Escala, Substituicao, Auditoria, Funcao, Local

@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'email', 'telefone', 'ativo', 'carga_horaria_maxima_semanal')
    list_filter = ('cargo', 'ativo')
    search_fields = ('nome', 'email')
    list_editable = ('ativo', 'carga_horaria_maxima_semanal')

@admin.register(Funcao)
class FuncaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)

@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'endereco')
    list_editable = ('ativo',)

@admin.register(Plantao)
class PlantaoAdmin(admin.ModelAdmin):
    list_display = ('data', 'hora_inicio', 'hora_fim', 'funcao', 'local', 'duracao_horas')
    list_filter = ('data', 'funcao', 'local')
    date_hierarchy = 'data'
    search_fields = ('funcao__nome', 'local__nome')
    
    def duracao_horas(self, obj):
        return f"{obj.duracao_horas()}h"
    duracao_horas.short_description = 'Duração'

@admin.register(Escala)
class EscalaAdmin(admin.ModelAdmin):
    list_display = ('id_plantao', 'id_profissional', 'status', 'data_alocacao')
    list_filter = ('status', 'data_alocacao', 'id_profissional__cargo')
    raw_id_fields = ('id_plantao', 'id_profissional')
    search_fields = ('id_profissional__nome', 'id_plantao__funcao__nome')

@admin.register(Substituicao)
class SubstituicaoAdmin(admin.ModelAdmin):
    list_display = ('id_escala_original', 'id_profissional_solicitante', 'id_profissional_substituto', 'status', 'data_solicitacao')
    list_filter = ('status', 'data_solicitacao')
    raw_id_fields = ('id_escala_original', 'id_profissional_solicitante', 'id_profissional_substituto')
    search_fields = (
        'id_profissional_solicitante__nome', 
        'id_profissional_substituto__nome',
        'id_escala_original__id_plantao__funcao__nome'
    )

@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('entidade', 'id_entidade', 'acao', 'usuario', 'data_hora')
    list_filter = ('entidade', 'acao', 'usuario')
    readonly_fields = ('data_hora',)
    search_fields = ('entidade', 'acao', 'usuario')