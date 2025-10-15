"""
seed_data_sql.py

Comando customizado do Django para popular o banco de dados
com dados iniciais de escala, lidos de escala360_seed.py.

Para rodar: python manage.py seed_data_sql
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from escala_app.models import (
    Profissional, Plantao, Escala, Substituicao, Auditoria,
    Funcao, Local
)
# Importa os dados parseados
from escala_app.fixtures.escala_seed import (
    FUNCAO_DATA, LOCAL_DATA, PROFISSIONAIS_DATA, PLANTOES_DATA, 
    ESCALAS_DATA, SUBSTITUICOES_DATA, AUDITORIA_DATA, CARGO_MAP
)

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais baseados no escala360.sql, incluindo Funcao e Local.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Iniciando a limpeza e população do banco de dados...'))

        try:
            with transaction.atomic():
                # ----------------------------------------------------
                # Limpeza em ordem reversa de dependência
                # ----------------------------------------------------
                Auditoria.objects.all().delete()
                Substituicao.objects.all().delete()
                Escala.objects.all().delete()
                Plantao.objects.all().delete()
                Profissional.objects.all().delete()
                Funcao.objects.all().delete()
                Local.objects.all().delete()
                
                self.stdout.write(self.style.SUCCESS('Limpeza das tabelas concluída.'))

                # Mapeamentos de ID para Objeto para as FKs
                funcoes_map = {}
                locais_map = {}

                # ----------------------------------------------------
                # 0. População das tabelas de suporte (Funcao e Local)
                # O script usa os IDs exatos definidos no seed
                # ----------------------------------------------------
                for data in FUNCAO_DATA:
                    obj = Funcao.objects.create(id=data['id'], nome=data['nome'])
                    funcoes_map[data['id']] = obj
                self.stdout.write(self.style.SUCCESS(f'População de {len(FUNCAO_DATA)} Funções concluída.'))

                for data in LOCAL_DATA:
                    obj = Local.objects.create(id=data['id'], nome=data['nome'])
                    locais_map[data['id']] = obj
                self.stdout.write(self.style.SUCCESS(f'População de {len(LOCAL_DATA)} Locais concluída.'))


                # ----------------------------------------------------
                # 1. População de Profissionais
                # ----------------------------------------------------
                for data in PROFISSIONAIS_DATA:
                    # Usa o valor exato do SQL, que deve estar no ProfissionalChoices
                    cargo_value = CARGO_MAP.get(data['cargo'], data['cargo'])
                    Profissional.objects.create(
                        id=data['id'],
                        nome=data['nome'],
                        cargo=cargo_value,
                        email=data['email'],
                        telefone=data['telefone'] if data['telefone'] else None,
                        ativo=data['ativo']
                    )
                self.stdout.write(self.style.SUCCESS(f'População de {len(PROFISSIONAIS_DATA)} Profissionais concluída.'))
                
                # ----------------------------------------------------
                # 2. População de Plantões
                # ----------------------------------------------------
                for data in PLANTOES_DATA:
                    # Garante que as FKs sejam resolvidas com os objetos criados acima
                    Plantao.objects.create(
                        id=data['id'],
                        data=data['data'],
                        hora_inicio=data['hora_inicio'],
                        hora_fim=data['hora_fim'],
                        funcao=funcoes_map.get(data['id_funcao']),
                        # O SQL só usa id_local=1. Usamos local_map[1]
                        local=locais_map.get(data['id_local'])
                    )
                self.stdout.write(self.style.SUCCESS(f'População de {len(PLANTOES_DATA)} Plantões concluída.'))

                # ----------------------------------------------------
                # 3. População de Escalas
                # ----------------------------------------------------
                for data in ESCALAS_DATA:
                    Escala.objects.create(
                        id=data['id'],
                        plantao=Plantao.objects.get(id=data['id_plantao']),
                        profissional=Profissional.objects.get(id=data['id_profissional']),
                        status=data['status'],
                    )
                self.stdout.write(self.style.SUCCESS(f'População de {len(ESCALAS_DATA)} Escalas concluída.'))

                # ----------------------------------------------------
                # 4. População de Substituições
                # ----------------------------------------------------
                for data in SUBSTITUICOES_DATA:
                    Substituicao.objects.create(
                        id=data['id'],
                        escala_original=Escala.objects.get(id=data['id_escala_original']),
                        profissional_solicitante=Profissional.objects.get(id=data['id_profissional_solicitante']),
                        profissional_substituto=Profissional.objects.get(id=data['id_profissional_substituto']),
                        status=data['status']
                    )
                self.stdout.write(self.style.SUCCESS(f'População de {len(SUBSTITUICOES_DATA)} Substituições concluída.'))

                # ----------------------------------------------------
                # 5. População de Auditoria
                # ----------------------------------------------------
                for data in AUDITORIA_DATA:
                    Auditoria.objects.create(
                        id=data['id'],
                        entidade=data['entidade'],
                        id_entidade=data['id_entidade'],
                        acao=data['acao'],
                        usuario=data['usuario']
                    )
                self.stdout.write(self.style.SUCCESS(f'População de {len(AUDITORIA_DATA)} Registros de Auditoria concluída.'))

                self.stdout.write(self.style.SUCCESS('\n>>> Migração e População de Dados concluídas com sucesso! <<<'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ocorreu um erro durante a população: {e}'))
