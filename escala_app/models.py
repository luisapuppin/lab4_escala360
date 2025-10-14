from django.db import models

# Create your models here.

# Definições de Status (Fidelidade ao SQL original)
STATUS_ESCALA_CHOICES = [
    ('ativo', 'Ativo (Alocado)'),
    ('substituido', 'Substituído'),
    ('solicit_subst', 'Solicitando Substituição'),
]

STATUS_SUBSTITUICAO_CHOICES = [
    ('pendente', 'Pendente de Aprovação'),
    ('aprovado', 'Aprovado'),
    ('rejeitado', 'Rejeitado'),
]

# Definições de Ação para Auditoria
ACAO_AUDITORIA_CHOICES = [
    ('criado', 'Criado'),
    ('aprovado', 'Aprovado'),
    ('excluido', 'Excluído'),
    ('alterado', 'Alterado'),
]

class Profissional(models.Model):
    # Corresponde à tabela 'profissionais'
    nome = models.CharField(max_length=255, null=False)
    cargo = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True, null=False)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    # Adicionado campo de Carga Horária (Regra 1 do documento)
    carga_horaria_maxima_semanal = models.IntegerField(default=40)

    class Meta:
        verbose_name_plural = "Profissionais"
        # Garante que o nome da tabela seja 'profissionais' (se estiver usando DBs que suportam isso)
        # Se for SQLite, o nome será 'escala_app_profissional'

    def __str__(self):
        return f"{self.nome} ({self.cargo})"

class Plantao(models.Model):
    # Corresponde à tabela 'plantoes'
    data = models.DateField(null=False)
    hora_inicio = models.TimeField(null=False)
    hora_fim = models.TimeField(null=False)
    
    # Mantidos como INTEGER, pois Funcao e Local não têm modelos FK definidos
    id_funcao = models.IntegerField(null=False) 
    id_local = models.IntegerField(null=False)

    class Meta:
        verbose_name_plural = "Plantões"

    def __str__(self):
        return f"Plantão {self.data} de {self.hora_inicio} a {self.hora_fim}"

class Escala(models.Model):
    # Corresponde à tabela 'escalas'
    plantao = models.ForeignKey(Plantao, on_delete=models.CASCADE, related_name='escalas')
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='escalas')
    status = models.CharField(
        max_length=20,
        choices=STATUS_ESCALA_CHOICES,
        default='ativo' # Usa o status 'ativo' do SQL
    )
    data_alocacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Escalas"
        unique_together = ('plantao', 'profissional') # Regra de unicidade

    def __str__(self):
        return f"Escala: {self.profissional.nome} - {self.plantao}"

class Substituicao(models.Model):
    # Corresponde à tabela 'substituicoes'
    escala_original = models.ForeignKey(Escala, on_delete=models.CASCADE, related_name='substituicao_original')
    profissional_solicitante = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='substituicoes_solicitadas')
    # O substituto pode ser null se a solicitação estiver pendente
    profissional_substituto = models.ForeignKey(Profissional, on_delete=models.SET_NULL, related_name='substituicoes_realizadas', null=True, blank=True)
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15,
        choices=STATUS_SUBSTITUICAO_CHOICES,
        default='pendente' # Usa o status 'pendente' do SQL
    )
    # Campo adicional para rastrear aprovação (Implícito na Regra 3)
    aprovada_por_supervisor = models.BooleanField(default=False) 

    class Meta:
        verbose_name_plural = "Substituições"

    def __str__(self):
        return f"Subst. {self.escala_original_id} - Status: {self.status}"

class Auditoria(models.Model):
    # Corresponde à tabela 'auditoria'
    entidade = models.CharField(max_length=50, null=False)
    id_entidade = models.IntegerField(null=False)
    acao = models.CharField(
        max_length=20, 
        choices=ACAO_AUDITORIA_CHOICES,
        null=False
    )
    usuario = models.CharField(max_length=100, null=False)
    data_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Auditorias"

    def __str__(self):
        return f"Auditoria: {self.entidade}/{self.id_entidade} - {self.acao}"
