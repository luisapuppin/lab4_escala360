# escala360/management/commands/importar_dados_sql.py
from django.core.management.base import BaseCommand
from django.db import connection
from datetime import datetime
from escala360.models import Profissional, Plantao, Escala, Substituicao, Auditoria, Funcao, Local

class Command(BaseCommand):
    help = 'Importa dados do arquivo SQL para o banco SQLite'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando importação de dados...')
        
        # Limpar dados existentes (opcional - comente se não quiser limpar)
        self.limpar_dados()
        
        # Importar profissionais
        self.importar_profissionais()
        
        # Importar plantões
        self.importar_plantoes()
        
        # Importar escalas
        self.importar_escalas()
        
        # Importar substituições
        self.importar_substituicoes()
        
        # Importar auditoria
        self.importar_auditoria()
        
        self.stdout.write(
            self.style.SUCCESS('Dados importados com sucesso!')
        )

    def limpar_dados(self):
        """Limpa todos os dados existentes"""
        self.stdout.write('Limpando dados existentes...')
        Auditoria.objects.all().delete()
        Substituicao.objects.all().delete()
        Escala.objects.all().delete()
        Plantao.objects.all().delete()
        Profissional.objects.all().delete()

    def importar_profissionais(self):
        """Importa dados da tabela profissionais"""
        profissionais_data = [
            ('Ana Souza', 'Enfermeira', 'ana.souza@example.com', '11999990001', True, 40),
            ('Carlos Lima', 'Médico', 'carlos.lima@example.com', '11999990002', True, 40),
            ('Beatriz Santos', 'Técnico de Enfermagem', 'beatriz.santos@example.com', '11999990003', True, 40),
            ('Daniel Oliveira', 'Médico', 'daniel.oliveira@example.com', '11999990004', True, 40),
            ('Fernanda Costa', 'Enfermeira', 'fernanda.costa@example.com', '11999990005', True, 40),
            ('Gustavo Nunes', 'Médico', 'gustavo.nunes@example.com', '11999990006', True, 40),
            ('Helena Duarte', 'Enfermeira', 'helena.duarte@example.com', '11999990007', True, 40),
            ('Igor Martins', 'Técnico de Enfermagem', 'igor.martins@example.com', '11999990008', True, 40),
            ('Juliana Rocha', 'Enfermeira', 'juliana.rocha@example.com', '11999990009', True, 40),
            ('Kaique Barbosa', 'Médico', 'kaique.barbosa@example.com', '11999990010', True, 40),
            ('Larissa Ribeiro', 'Enfermeira', 'larissa.ribeiro@example.com', '11999990011', True, 40),
            ('Marcelo Vieira', 'Médico', 'marcelo.vieira@example.com', '11999990012', True, 40),
            ('Natália Almeida', 'Técnico de Enfermagem', 'natalia.almeida@example.com', '11999990013', True, 40),
            ('Otávio Mendes', 'Enfermeiro', 'otavio.mendes@example.com', '11999990014', True, 40),
            ('Patrícia Neves', 'Médica', 'patricia.neves@example.com', '11999990015', True, 40),
            ('Rafael Cunha', 'Médico', 'rafael.cunha@example.com', '11999990016', True, 40),
            ('Sabrina Lopes', 'Enfermeira', 'sabrina.lopes@example.com', '11999990017', True, 40),
            ('Thiago Freitas', 'Técnico de Enfermagem', 'thiago.freitas@example.com', '11999990018', True, 40),
            ('Vanessa Campos', 'Enfermeira', 'vanessa.campos@example.com', '11999990019', True, 40),
            ('William Costa', 'Médico', 'william.costa@example.com', '11999990020', True, 40),
            ('Yasmin Pires', 'Enfermeira', 'yasmin.pires@example.com', '11999990021', True, 40),
            ('Zeca Ferreira', 'Técnico de Enfermagem', 'zeca.ferreira@example.com', '11999990022', True, 40),
            ('Bruno Teixeira', 'Médico', 'bruno.teixeira@example.com', '11999990023', True, 40),
            ('Clara Cardoso', 'Enfermeira', 'clara.cardoso@example.com', '11999990024', True, 40),
            ('Diego Melo', 'Médico', 'diego.melo@example.com', '11999990025', True, 40),
            ('Eduarda Batista', 'Enfermeira', 'eduarda.batista@example.com', '11999990026', True, 40),
            ('Felipe Braga', 'Médico', 'felipe.braga@example.com', '11999990027', True, 40),
            ('Giovana Reis', 'Técnico de Enfermagem', 'giovana.reis@example.com', '11999990028', True, 40),
            ('Hugo Sales', 'Médico', 'hugo.sales@example.com', '11999990029', True, 40),
            ('Isabela Farias', 'Enfermeira', 'isabela.farias@example.com', '11999990030', True, 40),
        ]

        for nome, cargo, email, telefone, ativo, carga_maxima in profissionais_data:
            Profissional.objects.create(
                nome=nome,
                cargo=cargo,
                email=email,
                telefone=telefone,
                ativo=ativo,
                carga_horaria_maxima_semanal=carga_maxima
            )

        self.stdout.write(f'✓ {len(profissionais_data)} profissionais importados')

    def importar_plantoes(self):
        """Importa dados da tabela plantoes e retorna dicionário mapeando IDs antigos para novos"""
        # Primeiro, criar funções e locais padrão se não existirem
        funcao_medico, _ = Funcao.objects.get_or_create(nome="Médico", defaults={'descricao': 'Profissional médico'})
        funcao_enfermeiro, _ = Funcao.objects.get_or_create(nome="Enfermeiro", defaults={'descricao': 'Profissional de enfermagem'})
        funcao_tecnico, _ = Funcao.objects.get_or_create(nome="Técnico de Enfermagem", defaults={'descricao': 'Técnico de enfermagem'})
        
        local_principal, _ = Local.objects.get_or_create(nome="Pronto Socorro", defaults={'endereco': 'Local principal'})
        
        plantoes_data = [
            (1, '2025-07-01', '08:00', '14:00', funcao_enfermeiro, local_principal),
            (2, '2025-07-01', '14:00', '20:00', funcao_enfermeiro, local_principal),
            (3, '2025-07-02', '08:00', '14:00', funcao_medico, local_principal),
            (4, '2025-07-02', '14:00', '20:00', funcao_medico, local_principal),
            (5, '2025-07-03', '08:00', '14:00', funcao_enfermeiro, local_principal),
            (6, '2025-07-03', '14:00', '20:00', funcao_enfermeiro, local_principal),
            (7, '2025-07-04', '08:00', '14:00', funcao_medico, local_principal),
            (8, '2025-07-04', '14:00', '20:00', funcao_medico, local_principal),
            (9, '2025-07-05', '08:00', '14:00', funcao_enfermeiro, local_principal),
            (10, '2025-07-05', '14:00', '20:00', funcao_enfermeiro, local_principal),
            (11, '2025-07-06', '08:00', '14:00', funcao_medico, local_principal),
            (12, '2025-07-06', '14:00', '20:00', funcao_medico, local_principal),
            (13, '2025-07-07', '08:00', '14:00', funcao_enfermeiro, local_principal),
            (14, '2025-07-07', '14:00', '20:00', funcao_enfermeiro, local_principal),
            (15, '2025-07-08', '08:00', '14:00', funcao_medico, local_principal),
            (16, '2025-07-08', '14:00', '20:00', funcao_medico, local_principal),
            (17, '2025-07-09', '08:00', '14:00', funcao_enfermeiro, local_principal),
            (18, '2025-07-09', '14:00', '20:00', funcao_enfermeiro, local_principal),
            (19, '2025-07-10', '08:00', '14:00', funcao_medico, local_principal),
            (20, '2025-07-10', '14:00', '20:00', funcao_medico, local_principal),
        ]

        plantoes_map = {}
        for id_antigo, data, hora_inicio, hora_fim, funcao, local in plantoes_data:
            plantao = Plantao.objects.create(
                data=datetime.strptime(data, '%Y-%m-%d').date(),
                hora_inicio=datetime.strptime(hora_inicio, '%H:%M').time(),
                hora_fim=datetime.strptime(hora_fim, '%H:%M').time(),
                funcao=funcao,
                local=local
            )
            plantoes_map[id_antigo] = plantao.id

        self.stdout.write(f'✓ {len(plantoes_data)} plantões importados')
        return plantoes_map

    def importar_escalas(self):
        """Importa dados da tabela escalas"""
        escalas_data = [
            (1, 1, 'ativo'),
            (2, 2, 'ativo'),
            (3, 3, 'ativo'),
            (4, 4, 'ativo'),
            (5, 5, 'ativo'),
            (6, 6, 'ativo'),
            (7, 7, 'ativo'),
            (8, 8, 'ativo'),
            (9, 9, 'ativo'),
            (10, 10, 'ativo'),
            (11, 11, 'ativo'),
            (12, 12, 'ativo'),
            (13, 13, 'ativo'),
            (14, 14, 'ativo'),
            (15, 15, 'ativo'),
            (16, 16, 'ativo'),
            (17, 17, 'ativo'),
            (18, 18, 'ativo'),
            (19, 19, 'ativo'),
            (20, 20, 'ativo'),
        ]

        for id_plantao, id_profissional, status in escalas_data:
            try:
                plantao = Plantao.objects.get(id=id_plantao)
                profissional = Profissional.objects.get(id=id_profissional)
                
                Escala.objects.create(
                    id_plantao=plantao,
                    id_profissional=profissional,
                    status=status
                )
            except (Plantao.DoesNotExist, Profissional.DoesNotExist) as e:
                self.stdout.write(
                    self.style.WARNING(f'Erro ao criar escala {id_plantao}-{id_profissional}: {e}')
                )

        self.stdout.write(f'✓ {len(escalas_data)} escalas importadas')

    def importar_substituicoes(self):
        """Importa dados da tabela substituicoes"""
        substituicoes_data = [
            (2, 2, 4, 'pendente'),
            (3, 3, 5, 'aprovado'),
            (4, 4, 6, 'pendente'),
            (5, 5, 7, 'pendente'),
            (6, 6, 8, 'aprovado'),
            (7, 7, 9, 'pendente'),
            (8, 8, 10, 'aprovado'),
        ]

        for id_escala_original, id_profissional_solicitante, id_profissional_substituto, status in substituicoes_data:
            try:
                escala_original = Escala.objects.get(id=id_escala_original)
                profissional_solicitante = Profissional.objects.get(id=id_profissional_solicitante)
                profissional_substituto = Profissional.objects.get(id=id_profissional_substituto)
                
                Substituicao.objects.create(
                    id_escala_original=escala_original,
                    id_profissional_solicitante=profissional_solicitante,
                    id_profissional_substituto=profissional_substituto,
                    status=status
                )
            except (Escala.DoesNotExist, Profissional.DoesNotExist) as e:
                self.stdout.write(
                    self.style.WARNING(f'Erro ao criar substituição {id_escala_original}: {e}')
                )

        self.stdout.write(f'✓ {len(substituicoes_data)} substituições importadas')

    def importar_auditoria(self):
        """Importa dados da tabela auditoria"""
        auditoria_data = [
            ('substituicao', 1, 'criado', 'sistema'),
            ('substituicao', 2, 'aprovado', 'supervisor'),
            ('substituicao', 3, 'criado', 'sistema'),
            ('substituicao', 4, 'criado', 'sistema'),
            ('substituicao', 5, 'criado', 'sistema'),
            ('substituicao', 6, 'criado', 'sistema'),
            ('substituicao', 7, 'aprovado', 'supervisor'),
            ('escala', 1, 'criado', 'sistema'),
            ('escala', 2, 'criado', 'sistema'),
            ('escala', 3, 'criado', 'sistema'),
            ('escala', 4, 'criado', 'sistema'),
            ('escala', 5, 'criado', 'sistema'),
            ('escala', 6, 'criado', 'sistema'),
            ('escala', 7, 'criado', 'sistema'),
            ('escala', 8, 'criado', 'sistema'),
        ]

        for entidade, id_entidade, acao, usuario in auditoria_data:
            Auditoria.objects.create(
                entidade=entidade,
                id_entidade=id_entidade,
                acao=acao,
                usuario=usuario
            )

        self.stdout.write(f'✓ {len(auditoria_data)} registros de auditoria importados')
