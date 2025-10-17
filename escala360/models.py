from django.db import models

# Create your models here.

# escala360/models.py
from django.db import models

class Funcao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    
    def __str__(self):
        return self.nome

class Local(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome

class Profissional(models.Model):
    nome = models.CharField(max_length=200)
    cargo = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    carga_horaria_maxima_semanal = models.IntegerField(default=40)
    
    class Meta:
        verbose_name_plural = "Profissionais"
    
    def horas_trabalhadas_semana(self, data_referencia=None):
        """Calcula horas trabalhadas na semana de uma data específica"""
        from datetime import datetime, timedelta
        from django.utils import timezone
        
        # Se não for fornecida uma data de referência, usa a data atual
        if data_referencia is None:
            data_referencia = timezone.now().date()
        else:
            # Garantir que é um objeto date
            if isinstance(data_referencia, str):
                data_referencia = datetime.strptime(data_referencia, '%Y-%m-%d').date()
        
        # Calcular início e fim da semana da data de referência
        inicio_semana = data_referencia - timedelta(days=data_referencia.weekday())
        fim_semana = inicio_semana + timedelta(days=6)
        
        # Debug: verificar o período
        print(f"DEBUG: Calculando horas para {self.nome} - período: {inicio_semana} a {fim_semana} (referência: {data_referencia})")
        
        # Buscar todas as escalas ativas do profissional na semana da data de referência
        escalas_semana = Escala.objects.filter(
            id_profissional=self,
            id_plantao__data__gte=inicio_semana,
            id_plantao__data__lte=fim_semana,
            status='ativo'
        ).select_related('id_plantao')
        
        print(f"DEBUG: {escalas_semana.count()} escalas encontradas")
        
        horas_trabalhadas = 0
        
        for escala in escalas_semana:
            plantao = escala.id_plantao
            
            # Converter para datetime para calcular diferença
            inicio_dt = datetime.combine(plantao.data, plantao.hora_inicio)
            fim_dt = datetime.combine(plantao.data, plantao.hora_fim)
            
            # Calcular diferença em horas
            diferenca = fim_dt - inicio_dt
            horas_plantao = diferenca.total_seconds() / 3600
            
            horas_trabalhadas += horas_plantao
            
            print(f"DEBUG: Plantão {plantao.id} - {plantao.data} {plantao.hora_inicio}-{plantao.hora_fim} = {horas_plantao}h")
        
        resultado = round(horas_trabalhadas, 2)
        print(f"DEBUG: Total final: {resultado}h")
        
        return resultado
    
    def __str__(self):
        return f"{self.nome} - {self.cargo}"

class Plantao(models.Model):
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    funcao = models.ForeignKey(Funcao, on_delete=models.CASCADE)
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Plantões"
    
    def __str__(self):
        return f"Plantão {self.id} - {self.data} ({self.hora_inicio} às {self.hora_fim})"
    
    def duracao_horas(self):
        """Calcula a duração do plantão em horas"""
        from datetime import datetime
        inicio = datetime.combine(self.data, self.hora_inicio)
        fim = datetime.combine(self.data, self.hora_fim)
        return round((fim - inicio).seconds / 3600, 2)

class Escala(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('substituido', 'Substituído'),
    ]
    
    id_plantao = models.ForeignKey(Plantao, on_delete=models.CASCADE)
    id_profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    data_alocacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Escala {self.id} - {self.id_profissional.nome}"

class Substituicao(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]
    
    id_escala_original = models.ForeignKey(Escala, on_delete=models.CASCADE, related_name='substituicoes_originais')
    id_profissional_solicitante = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='substituicoes_solicitadas')
    id_profissional_substituto = models.ForeignKey(Profissional, on_delete=models.CASCADE, related_name='substituicoes_substituidas')
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    
    class Meta:
        verbose_name_plural = "Substituições"
    
    def __str__(self):
        return f"Substituição {self.id} - {self.id_profissional_solicitante.nome} → {self.id_profissional_substituto.nome}"

class Auditoria(models.Model):
    entidade = models.CharField(max_length=100)
    id_entidade = models.IntegerField()
    acao = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    data_hora = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Auditoria {self.id} - {self.entidade}.{self.id_entidade} - {self.acao}"
    