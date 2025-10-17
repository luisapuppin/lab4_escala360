# escala360/management/commands/criar_funcoes_locais.py
from django.core.management.base import BaseCommand
from escala360.models import Funcao, Local

class Command(BaseCommand):
    help = 'Cria funções e locais iniciais para o sistema'

    def handle(self, *args, **options):
        # Criar funções
        funcoes = [
            ('Médico', 'Profissional médico responsável por atendimentos'),
            ('Enfermeiro', 'Profissional de enfermagem de nível superior'),
            ('Técnico de Enfermagem', 'Profissional de enfermagem de nível técnico'),
            ('Recepcionista', 'Profissional de atendimento ao público'),
        ]
        
        for nome, descricao in funcoes:
            Funcao.objects.get_or_create(
                nome=nome,
                defaults={'descricao': descricao}
            )
        
        # Criar locais
        locais = [
            ('Pronto Socorro', 'Av. Principal, 123 - Centro'),
            ('UTI', 'Av. Principal, 123 - 2º andar'),
            ('Enfermaria A', 'Av. Principal, 123 - Ala A'),
            ('Enfermaria B', 'Av. Principal, 123 - Ala B'),
            ('Ambulatório', 'Av. Principal, 123 - Térreo'),
        ]
        
        for nome, endereco in locais:
            Local.objects.get_or_create(
                nome=nome,
                defaults={'endereco': endereco}
            )
        
        self.stdout.write(
            self.style.SUCCESS('Funções e locais criados com sucesso!')
        )