# escala360/forms.py
from django import forms
from .models import Escala, Plantao, Profissional, Funcao, Local
from datetime import datetime, time
from django.utils import timezone

class PlantaoForm(forms.ModelForm):
    class Meta:
        model = Plantao
        fields = ['data', 'hora_inicio', 'hora_fim', 'funcao', 'local']
        widgets = {
            'data': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': timezone.now().date().isoformat()
            }),
            'hora_inicio': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'hora_fim': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'funcao': forms.Select(attrs={'class': 'form-control'}),
            'local': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fim = cleaned_data.get('hora_fim')
        
        if data and hora_inicio and hora_fim:
            # Verificar se a data não é no passado
            if data < timezone.now().date():
                raise forms.ValidationError("Não é possível cadastrar plantões em datas passadas.")
            
            # Verificar se horário de fim é depois do horário de início
            if hora_fim <= hora_inicio:
                raise forms.ValidationError("O horário de fim deve ser após o horário de início.")
            
            # Verificar duração mínima (1 hora)
            inicio_dt = datetime.combine(data, hora_inicio)
            fim_dt = datetime.combine(data, hora_fim)
            duracao = (fim_dt - inicio_dt).seconds / 3600
            if duracao < 1:
                raise forms.ValidationError("O plantão deve ter duração mínima de 1 hora.")
        
        return cleaned_data

class EscalaForm(forms.ModelForm):
    class Meta:
        model = Escala
        fields = ['id_profissional']
        widgets = {
            'id_profissional': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar com todos os profissionais ativos
        self.fields['id_profissional'].queryset = Profissional.objects.filter(ativo=True)
        self.fields['id_profissional'].required = True