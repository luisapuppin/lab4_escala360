"""
escala_seed.py

Dados de população extraídos e parseados do arquivo escala360.sql,
incluindo sugestões concretas para Funcao e Local.
"""

# Mapeamento de cargos brutos do SQL para o formato do Django Choices (mantido)
CARGO_MAP = {
    'Enfermeira': 'Enfermeira',
    'Médico': 'Médico',
    'Médica': 'Médica',
    'Técnico de Enfermagem': 'Técnico de Enfermagem',
    'Enfermeiro': 'Enfermeiro', # Adiciona caso exista no SQL (embora não tenha sido visto)
}

# ----------------------------------------------------
# Funções (CRIADAS)
# ----------------------------------------------------
FUNCAO_DATA = [
    {'id': 1, 'nome': 'Médico (Plantão)'},
    {'id': 2, 'nome': 'Enfermagem (Plantão)'},
]

# ----------------------------------------------------
# Locais (CRIADOS)
# ----------------------------------------------------
LOCAL_DATA = [
    {'id': 1, 'nome': 'CTI/UTI'},
    {'id': 2, 'nome': 'Emergência'},
    {'id': 3, 'nome': 'Enfermaria'},
]

# ----------------------------------------------------
# Profissionais (30 registros) - Dados mantidos
# ----------------------------------------------------
PROFISSIONAIS_DATA = [
    {'id': 1, 'nome': 'Ana Souza', 'cargo': 'Enfermeira', 'email': 'ana.souza@example.com', 'telefone': '11999990001', 'ativo': True},
    {'id': 2, 'nome': 'Carlos Lima', 'cargo': 'Médico', 'email': 'carlos.lima@example.com', 'telefone': '11999990002', 'ativo': True},
    {'id': 3, 'nome': 'Beatriz Santos', 'cargo': 'Técnico de Enfermagem', 'email': 'beatriz.santos@example.com', 'telefone': '11999990003', 'ativo': True},
    {'id': 4, 'nome': 'Daniel Oliveira', 'cargo': 'Médico', 'email': 'daniel.oliveira@example.com', 'telefone': '11999990004', 'ativo': True},
    {'id': 5, 'nome': 'Fernanda Costa', 'cargo': 'Enfermeira', 'email': 'fernanda.costa@example.com', 'telefone': '11999990005', 'ativo': True},
    {'id': 6, 'nome': 'Gustavo Nunes', 'cargo': 'Médico', 'email': 'gustavo.nunes@example.com', 'telefone': '11999990006', 'ativo': True},
    {'id': 7, 'nome': 'Helena Duarte', 'cargo': 'Enfermeira', 'email': 'helena.duarte@example.com', 'telefone': '11999990007', 'ativo': True},
    {'id': 8, 'nome': 'Igor Martins', 'cargo': 'Técnico de Enfermagem', 'email': 'igor.martins@example.com', 'telefone': '11999990008', 'ativo': True},
    {'id': 9, 'nome': 'Juliana Rocha', 'cargo': 'Enfermeira', 'email': 'juliana.rocha@example.com', 'telefone': '11999990009', 'ativo': True},
    {'id': 10, 'nome': 'Kaique Barbosa', 'cargo': 'Médico', 'email': 'kaique.barbosa@example.com', 'telefone': '11999990010', 'ativo': True},
    {'id': 11, 'nome': 'Larissa Ribeiro', 'cargo': 'Enfermeira', 'email': 'larissa.ribeiro@example.com', 'telefone': '11999990011', 'ativo': True},
    {'id': 12, 'nome': 'Marcelo Vieira', 'cargo': 'Médico', 'email': 'marcelo.vieira@example.com', 'telefone': '11999990012', 'ativo': True},
    {'id': 13, 'nome': 'Natália Almeida', 'cargo': 'Técnico de Enfermagem', 'email': 'natalia.almeida@example.com', 'telefone': '11999990013', 'ativo': True},
    {'id': 14, 'nome': 'Otávio Mendes', 'cargo': 'Enfermeiro', 'email': 'otavio.mendes@example.com', 'telefone': '11999990014', 'ativo': True},
    {'id': 15, 'nome': 'Patrícia Neves', 'cargo': 'Médica', 'email': 'patricia.neves@example.com', 'telefone': '11999990015', 'ativo': True},
    {'id': 16, 'nome': 'Rafael Cunha', 'cargo': 'Médico', 'email': 'rafael.cunha@example.com', 'telefone': '11999990016', 'ativo': True},
    {'id': 17, 'nome': 'Sabrina Lopes', 'cargo': 'Enfermeira', 'email': 'sabrina.lopes@example.com', 'telefone': '11999990017', 'ativo': True},
    {'id': 18, 'nome': 'Thiago Freitas', 'cargo': 'Técnico de Enfermagem', 'email': 'thiago.freitas@example.com', 'telefone': '11999990018', 'ativo': True},
    {'id': 19, 'nome': 'Vanessa Campos', 'cargo': 'Enfermeira', 'email': 'vanessa.campos@example.com', 'telefone': '11999990019', 'ativo': True},
    {'id': 20, 'nome': 'William Costa', 'cargo': 'Médico', 'email': 'william.costa@example.com', 'telefone': '11999990020', 'ativo': True},
    {'id': 21, 'nome': 'Yasmin Pires', 'cargo': 'Enfermeira', 'email': 'yasmin.pires@example.com', 'telefone': '11999990021', 'ativo': True},
    {'id': 22, 'nome': 'Zeca Ferreira', 'cargo': 'Técnico de Enfermagem', 'email': 'zeca.ferreira@example.com', 'telefone': '11999990022', 'ativo': True},
    {'id': 23, 'nome': 'Bruno Teixeira', 'cargo': 'Médico', 'email': 'bruno.teixeira@example.com', 'telefone': '11999990023', 'ativo': True},
    {'id': 24, 'nome': 'Clara Cardoso', 'cargo': 'Enfermeira', 'email': 'clara.cardoso@example.com', 'telefone': '11999990024', 'ativo': True},
    {'id': 25, 'nome': 'Diego Melo', 'cargo': 'Médico', 'email': 'diego.melo@example.com', 'telefone': '11999990025', 'ativo': True},
    {'id': 26, 'nome': 'Eduarda Batista', 'cargo': 'Enfermeira', 'email': 'eduarda.batista@example.com', 'telefone': '11999990026', 'ativo': True},
    {'id': 27, 'nome': 'Felipe Braga', 'cargo': 'Médico', 'email': 'felipe.braga@example.com', 'telefone': '11999990027', 'ativo': True},
    {'id': 28, 'nome': 'Giovana Reis', 'cargo': 'Técnico de Enfermagem', 'email': 'giovana.reis@example.com', 'telefone': '11999990028', 'ativo': True},
    {'id': 29, 'nome': 'Hugo Sales', 'cargo': 'Médico', 'email': 'hugo.sales@example.com', 'telefone': '11999990029', 'ativo': True},
    {'id': 30, 'nome': 'Isabela Farias', 'cargo': 'Enfermeira', 'email': 'isabela.farias@example.com', 'telefone': '11999990030', 'ativo': True},
]

# ----------------------------------------------------
# Plantões (20 registros) - Dados mantidos
# ----------------------------------------------------
PLANTOES_DATA = [
    # id_funcao=1 (Médico), id_local=1 (CTI/UTI)
    {'id': 1, 'data': '2025-07-01', 'hora_inicio': '08:00', 'hora_fim': '14:00', 'id_funcao': 1, 'id_local': 1},
    {'id': 2, 'data': '2025-07-01', 'hora_inicio': '14:00', 'hora_fim': '20:00', 'id_funcao': 1, 'id_local': 1},
    # id_funcao=2 (Enfermagem), id_local=1 (CTI/UTI)
    {'id': 3, 'data': '2025-07-02', 'hora_inicio': '08:00', 'hora_fim': '14:00', 'id_funcao': 2, 'id_local': 1},
    {'id': 4, 'data': '2025-07-02', 'hora_inicio': '14:00', 'hora_fim': '20:00', 'id_funcao': 2, 'id_local': 1},
    {'id': 5, 'data': '2025-07-03', 'hora_inicio': '08:00', 'hora_fim': '14:00', 'id_funcao': 1, 'id_local': 1},
    {'id': 6, 'data': '2025-07-03', 'hora_inicio': '14:00', 'hora_fim': '20:00', 'id_funcao': 1, 'id_local': 1},
    {'id': 7, 'data': '2025-07-04', 'hora_inicio': '08:00', 'hora_fim': '14:00', 'id_funcao': 2, 'id_local': 1},
    {'id': 8, 'data': '2025-07-04', 'hora_inicio': '14:00', 'hora_fim': '20:00', 'id_funcao': 2, 'id_local': 1},
    {'id': 9, 'data': '2025-07-05', 'hora_inicio': '08:00', 'hora_fim': '14:00', 'id_funcao': 1, 'id_local': 1},
    {'id': 10, 'data': '2025-07-05', 'hora_inicio': '14:00', 'hora_fim': '20:00', 'id_funcao': 1, 'id_local': 1},
    {'id': 11, 'data': '2025-07-06', 'hora_inicio': '08:00', 'hora_fim': '14:00', 'id_funcao': 2, 'id_local': 1},
    {'id': 12, 'data': '2025-07-06', 'hora_inicio': '14:00', 'hora_fim': '20:00', 'id_funcao': 2, 'id_local': 1},
    {'id': 13, 'data': '2025-07-07', 'hora_inicio': '08:00', 'hora_fim': '14:00', 'id_funcao': 1, 'id_local': 1},
    {'id': 14, 'data': '2025-07-07', 'hora_inicio': '14:00', 'hora_fim': '20:00', 'id_funcao': 1, 'id_local': 1},
    {'id': 15, 'data': '2025-07-08', 'hora_inicio': '08:00', 'hora_fim': '14:00', 'id_funcao': 2, 'id_local': 1},
    {'id': 16, 'data': '2025-07-08', 'hora_inicio': '14:00', 'hora_fim': '20:00', 'id_funcao': 2, 'id_local': 1},
    {'id': 17, 'data': '2025-07-09', 'hora_inicio': '08:00', 'hora_fim': '14:00', 'id_funcao': 1, 'id_local': 1},
    {'id': 18, 'data': '2025-07-09', 'hora_inicio': '14:00', 'hora_fim': '20:00', 'id_funcao': 1, 'id_local': 1},
    {'id': 19, 'data': '2025-07-10', 'hora_inicio': '08:00', 'hora_fim': '14:00', 'id_funcao': 2, 'id_local': 1},
    {'id': 20, 'data': '2025-07-10', 'hora_inicio': '14:00', 'hora_fim': '20:00', 'id_funcao': 2, 'id_local': 1},
]

# ----------------------------------------------------
# Escalas (20 registros) - Dados mantidos
# ----------------------------------------------------
ESCALAS_DATA = [
    {'id': 1, 'id_plantao': 1, 'id_profissional': 1, 'status': 'ativo'},
    {'id': 2, 'id_plantao': 2, 'id_profissional': 2, 'status': 'ativo'},
    {'id': 3, 'id_plantao': 3, 'id_profissional': 3, 'status': 'ativo'},
    {'id': 4, 'id_plantao': 4, 'id_profissional': 4, 'status': 'ativo'},
    {'id': 5, 'id_plantao': 5, 'id_profissional': 5, 'status': 'ativo'},
    {'id': 6, 'id_plantao': 6, 'id_profissional': 6, 'status': 'ativo'},
    {'id': 7, 'id_plantao': 7, 'id_profissional': 7, 'status': 'ativo'},
    {'id': 8, 'id_plantao': 8, 'id_profissional': 8, 'status': 'ativo'},
    {'id': 9, 'id_plantao': 9, 'id_profissional': 9, 'status': 'ativo'},
    {'id': 10, 'id_plantao': 10, 'id_profissional': 10, 'status': 'ativo'},
    {'id': 11, 'id_plantao': 11, 'id_profissional': 11, 'status': 'ativo'},
    {'id': 12, 'id_plantao': 12, 'id_profissional': 12, 'status': 'ativo'},
    {'id': 13, 'id_plantao': 13, 'id_profissional': 13, 'status': 'ativo'},
    {'id': 14, 'id_plantao': 14, 'id_profissional': 14, 'status': 'ativo'},
    {'id': 15, 'id_plantao': 15, 'id_profissional': 15, 'status': 'ativo'},
    {'id': 16, 'id_plantao': 16, 'id_profissional': 16, 'status': 'ativo'},
    {'id': 17, 'id_plantao': 17, 'id_profissional': 17, 'status': 'ativo'},
    {'id': 18, 'id_plantao': 18, 'id_profissional': 18, 'status': 'ativo'},
    {'id': 19, 'id_plantao': 19, 'id_profissional': 19, 'status': 'ativo'},
    {'id': 20, 'id_plantao': 20, 'id_profissional': 20, 'status': 'ativo'},
]

# ----------------------------------------------------
# Substituições (7 registros) - Dados mantidos
# ----------------------------------------------------
SUBSTITUICOES_DATA = [
    {'id': 1, 'id_escala_original': 2, 'id_profissional_solicitante': 2, 'id_profissional_substituto': 4, 'status': 'pendente'},
    {'id': 2, 'id_escala_original': 3, 'id_profissional_solicitante': 3, 'id_profissional_substituto': 5, 'status': 'aprovado'},
    {'id': 3, 'id_escala_original': 4, 'id_profissional_solicitante': 4, 'id_profissional_substituto': 6, 'status': 'pendente'},
    {'id': 4, 'id_escala_original': 5, 'id_profissional_solicitante': 5, 'id_profissional_substituto': 7, 'status': 'pendente'},
    {'id': 5, 'id_escala_original': 6, 'id_profissional_solicitante': 6, 'id_profissional_substituto': 8, 'status': 'aprovado'},
    {'id': 6, 'id_escala_original': 7, 'id_profissional_solicitante': 7, 'id_profissional_substituto': 9, 'status': 'pendente'},
    {'id': 7, 'id_escala_original': 8, 'id_profissional_solicitante': 8, 'id_profissional_substituto': 10, 'status': 'aprovado'},
]

# ----------------------------------------------------
# Auditoria (15 registros) - Dados mantidos
# ----------------------------------------------------
AUDITORIA_DATA = [
    {'id': 1, 'entidade': 'substituicao', 'id_entidade': 1, 'acao': 'criado', 'usuario': 'sistema'},
    {'id': 2, 'entidade': 'substituicao', 'id_entidade': 2, 'acao': 'aprovado', 'usuario': 'supervisor'},
    {'id': 3, 'entidade': 'substituicao', 'id_entidade': 3, 'acao': 'criado', 'usuario': 'sistema'},
    {'id': 4, 'entidade': 'substituicao', 'id_entidade': 4, 'acao': 'criado', 'usuario': 'sistema'},
    {'id': 5, 'entidade': 'substituicao', 'id_entidade': 5, 'acao': 'criado', 'usuario': 'sistema'},
    {'id': 6, 'entidade': 'substituicao', 'id_entidade': 6, 'acao': 'criado', 'usuario': 'sistema'},
    {'id': 7, 'entidade': 'substituicao', 'id_entidade': 7, 'acao': 'aprovado', 'usuario': 'supervisor'},
    {'id': 8, 'entidade': 'escala', 'id_entidade': 1, 'acao': 'criado', 'usuario': 'sistema'},
    {'id': 9, 'entidade': 'escala', 'id_entidade': 2, 'acao': 'criado', 'usuario': 'sistema'},
    {'id': 10, 'entidade': 'escala', 'id_entidade': 3, 'acao': 'criado', 'usuario': 'sistema'},
    {'id': 11, 'entidade': 'escala', 'id_entidade': 4, 'acao': 'criado', 'usuario': 'sistema'},
    {'id': 12, 'entidade': 'escala', 'id_entidade': 5, 'acao': 'criado', 'usuario': 'sistema'},
    {'id': 13, 'entidade': 'escala', 'id_entidade': 6, 'acao': 'criado', 'usuario': 'sistema'},
    {'id': 14, 'entidade': 'escala', 'id_entidade': 7, 'acao': 'criado', 'usuario': 'sistema'},
    {'id': 15, 'entidade': 'escala', 'id_entidade': 8, 'acao': 'criado', 'usuario': 'sistema'},
]
