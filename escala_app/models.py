"""
models.py
Define os modelos (tabelas) do banco de dados Django (SQLite).
As estruturas seguem estritamente o esquema SQL fornecido.
"""

from django.db import models

# Create your models here.

"""
models.py
Define os modelos (tabelas) do banco de dados Django (SQLite).
As estruturas seguem estritamente o esquema SQL fornecido.
"""

from django.db import models
from django.utils import timezone

# =========================================================
# DEFINIÇÕES DE CHOICES PARA PADRONIZAÇÃO DE DADOS
# =========================================================

class ProfissionalChoices(models.TextChoices):
    # Valores ajustados para bater com os dados do SQL (Médico, Médica, Enfermeira)
    MEDICO = 'Médico', 'Médico'
    MEDICA = 'Médica', 'Médica'
    ENFERMEIRO = 'Enfermeiro', 'Enfermeiro(a)' # Usado como fallback, mas o SQL usa 'Enfermeira'
    ENFERMEIRA = 'Enfermeira', 'Enfermeira'
    TEC_ENFERMAGEM = 'Técnico de Enfermagem', 'Técnico(a) de Enfermagem'

class EscalaStatusChoices(models.TextChoices):
    ATIVO = 'ativo', 'Ativo'
    SUBSTITUIDA = 'substituida', 'Substituída'
    CANCELADA = 'cancelada', 'Cancelada'

class SubstituicaoStatusChoices(models.TextChoices):
    PENDENTE = 'pendente', 'Pendente de Aprovação'
    APROVADO = 'aprovado', 'Aprovado'
    REJEITADO = 'rejeitado', 'Rejeitado'
    CANCELADO = 'cancelado', 'Cancelado'

class AuditoriaEntidadeChoices(models.TextChoices):
    SUBSTITUICAO = 'substituicao', 'Substituição'
    ESCALA = 'escala', 'Escala'

class AuditoriaAcaoChoices(models.TextChoices):
    CRIADO = 'criado', 'Criado'
    APROVADO = 'aprovado', 'Aprovado'
    REJEITADO = 'rejeitado', 'Rejeitado'
    CANCELADO = 'cancelado', 'Cancelado'
    EDITADO = 'editado', 'Editado'


# =========================================================
# MODELOS DE SUPORTE (Função e Local) - CRIADOS SIMPLES
# =========================================================

class Funcao(models.Model):
    """Representa a função requerida em um Plantão (e.g., Médico, Enfermeiro)."""
    nome = models.CharField(max_length=100, unique=True, verbose_name="Função no Plantão")
    class Meta:
        verbose_name_plural = "Funções"
        ordering = ['nome']
    def __str__(self):
        return self.nome

class Local(models.Model):
    """Representa o local físico onde o Plantão é realizado (e.g., CTI, Emergência)."""
    nome = models.CharField(max_length=100, unique=True, verbose_name="Local de Trabalho")
    class Meta:
        verbose_name_plural = "Locais"
        ordering = ['nome']
    def __str__(self):
        return self.nome


# =========================================================
# MODELO PRINCIPAL: Profissionais
# =========================================================

class Profissional(models.Model):
    """Corresponde à tabela 'profissionais' do SQL. Mantém o ID original."""
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255, null=False)
    cargo = models.CharField(
        max_length=50,
        choices=ProfissionalChoices.choices,
        null=False
    )
    email = models.EmailField(max_length=255, unique=True, null=False)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Profissionais"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.get_cargo_display()})"

# =========================================================
# MODELO PRINCIPAL: Plantões
# =========================================================

class Plantao(models.Model):
    """Corresponde à tabela 'plantoes' do SQL. Mantém o ID original."""
    id = models.IntegerField(primary_key=True)
    data = models.DateField(null=False)
    hora_inicio = models.TimeField(null=False)
    hora_fim = models.TimeField(null=False)

    # FKs para as novas tabelas de suporte
    funcao = models.ForeignKey(Funcao, on_delete=models.CASCADE, related_name='plantoes_necessarios')
    local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name='plantoes_alocados')

    class Meta:
        verbose_name_plural = "Plantões"
        ordering = ['data', 'hora_inicio']

    def __str__(self):
        return f"Plantão {self.local.nome} ({self.funcao.nome}) em {self.data.strftime('%d/%m/%Y')}"

# =========================================================
# MODELO PRINCIPAL: Escalas
# =========================================================

class Escala(models.Model):
    """Corresponde à tabela 'escalas' do SQL. Mantém o ID original."""
    id = models.IntegerField(primary_key=True)
    plantao = models.ForeignKey(Plantao, on_delete=models.CASCADE)
    profissional = models.ForeignKey(Profissional, on_delete=models.PROTECT, related_name='escalas_atribuidas')
    status = models.CharField(
        max_length=50,
        choices=EscalaStatusChoices.choices,
        default=EscalaStatusChoices.ATIVO
    )
    data_alocacao = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Escalas"
        # Adiciona a restrição que não pode ter o mesmo profissional no mesmo plantão
        unique_together = ('plantao', 'profissional')

    def __str__(self):
        return f"Escala {self.id}: {self.profissional.nome} no Plantão {self.plantao.id}"

# =========================================================
# MODELO PRINCIPAL: Substituições
# =========================================================

class Substituicao(models.Model):
    """Corresponde à tabela 'substituicoes' do SQL. Mantém o ID original."""
    id = models.IntegerField(primary_key=True)
    escala_original = models.ForeignKey(Escala, on_delete=models.PROTECT, related_name='substituicao_solicitada')
    profissional_solicitante = models.ForeignKey(Profissional, on_delete=models.PROTECT, related_name='solicitacoes_saida')
    profissional_substituto = models.ForeignKey(Profissional, on_delete=models.PROTECT, related_name='solicitacoes_entrada')
    data_solicitacao = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=50,
        choices=SubstituicaoStatusChoices.choices,
        default=SubstituicaoStatusChoices.PENDENTE
    )

    class Meta:
        verbose_name_plural = "Substituições"
        ordering = ['-data_solicitacao']

    def __str__(self):
        return f"Substituição {self.id} - Status: {self.get_status_display()}"

# =========================================================
# MODELO PRINCIPAL: Auditoria
# =========================================================

class Auditoria(models.Model):
    """Corresponde à tabela 'auditoria' do SQL. Mantém o ID original."""
    id = models.IntegerField(primary_key=True)
    entidade = models.CharField(
        max_length=50,
        choices=AuditoriaEntidadeChoices.choices,
        null=False
    )
    id_entidade = models.IntegerField(null=False)
    acao = models.CharField(
        max_length=50,
        choices=AuditoriaAcaoChoices.choices,
        null=False
    )
    usuario = models.CharField(max_length=255, null=False)
    data_hora = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Auditoria"
        ordering = ['-data_hora']

    def __str__(self):
        return f"Ação '{self.get_acao_display()}' em {self.get_entidade_display()} #{self.id_entidade}"
