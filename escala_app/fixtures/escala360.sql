-- Este arquivo contém apenas comandos INSERT, adaptados para os nomes das tabelas
-- criados pelo Django (ex: escala_app_profissional) e usando os status originais:
-- escalas.status = 'ativo'
-- substituicoes.status = 'pendente' ou 'aprovado'
-- Assumindo o id 1 do profissional é 'Ana Souza' e assim por diante.
-- O Django deve ser migrado antes de executar este script.

-- ===================================
-- Profissionais (30 registros)
-- Note que o nome da tabela muda: profissionais -> escala_app_profissional
-- Adicionado 'carga_horaria_maxima_semanal'
-- ===================================

INSERT INTO escala_app_profissional (id, nome, cargo, email, telefone, ativo, carga_horaria_maxima_semanal) VALUES
(1, 'Ana Souza', 'Enfermeira', 'ana.souza@example.com', '11999990001', 1, 40),
(2, 'Carlos Lima', 'Médico', 'carlos.lima@example.com', '11999990002', 1, 40),
(3, 'Beatriz Santos', 'Técnico de Enfermagem', 'beatriz.santos@example.com', '11999990003', 1, 40),
(4, 'Daniel Oliveira', 'Médico', 'daniel.oliveira@example.com', '11999990004', 1, 40),
(5, 'Fernanda Costa', 'Enfermeira', 'fernanda.costa@example.com', '11999990005', 1, 40),
(6, 'Gustavo Nunes', 'Médico', 'gustavo.nunes@example.com', '11999990006', 1, 40),
(7, 'Helena Duarte', 'Enfermeira', 'helena.duarte@example.com', '11999990007', 1, 40),
(8, 'Igor Martins', 'Técnico de Enfermagem', 'igor.martins@example.com', '11999990008', 1, 40),
(9, 'Juliana Rocha', 'Enfermeira', 'juliana.rocha@example.com', '11999990009', 1, 40),
(10, 'Kaique Barbosa', 'Médico', 'kaique.barbosa@example.com', '11999990010', 1, 40),
(11, 'Larissa Ribeiro', 'Enfermeira', 'larissa.ribeiro@example.com', '11999990011', 1, 40),
(12, 'Marcelo Vieira', 'Médico', 'marcelo.vieira@example.com', '11999990012', 1, 40),
(13, 'Natália Almeida', 'Técnico de Enfermagem', 'natalia.almeida@example.com', '11999990013', 1, 40),
(14, 'Otávio Mendes', 'Enfermeiro', 'otavio.mendes@example.com', '11999990014', 1, 40),
(15, 'Patrícia Neves', 'Médica', 'patricia.neves@example.com', '11999990015', 1, 40),
(16, 'Rafael Cunha', 'Médico', 'rafael.cunha@example.com', '11999990016', 1, 40),
(17, 'Sabrina Lopes', 'Enfermeira', 'sabrina.lopes@example.com', '11999990017', 1, 40),
(18, 'Thiago Freitas', 'Técnico de Enfermagem', 'thiago.freitas@example.com', '11999990018', 1, 40),
(19, 'Vanessa Campos', 'Enfermeira', 'vanessa.campos@example.com', '11999990019', 1, 40),
(20, 'William Costa', 'Médico', 'william.costa@example.com', '11999990020', 1, 40),
(21, 'Yasmin Pires', 'Enfermeira', 'yasmin.pires@example.com', '11999990021', 1, 40),
(22, 'Zeca Ferreira', 'Técnico de Enfermagem', 'zeca.ferreira@example.com', '11999990022', 1, 40),
(23, 'Bruno Teixeira', 'Médico', 'bruno.teixeira@example.com', '11999990023', 1, 40),
(24, 'Clara Cardoso', 'Enfermeira', 'clara.cardoso@example.com', '11999990024', 1, 40),
(25, 'Diego Melo', 'Médico', 'diego.melo@example.com', '11999990025', 1, 40),
(26, 'Eduarda Batista', 'Enfermeira', 'eduarda.batista@example.com', '11999990026', 1, 40),
(27, 'Felipe Braga', 'Médico', 'felipe.braga@example.com', '11999990027', 1, 40),
(28, 'Giovana Reis', 'Técnico de Enfermagem', 'giovana.reis@example.com', '11999990028', 1, 40),
(29, 'Hugo Sales', 'Médico', 'hugo.sales@example.com', '11999990029', 1, 40),
(30, 'Isabela Farias', 'Enfermeira', 'isabela.farias@example.com', '11999990030', 1, 40);

-- ===================================
-- Plantões (20 registros)
-- Note que o nome da tabela muda: plantoes -> escala_app_plantao
-- id_funcao e id_local são os campos do model
-- ===================================

INSERT INTO escala_app_plantao (id, data, hora_inicio, hora_fim, id_funcao, id_local) VALUES
(1, '2025-07-01', '08:00:00', '14:00:00', 1, 1),
(2, '2025-07-01', '14:00:00', '20:00:00', 1, 1),
(3, '2025-07-02', '08:00:00', '14:00:00', 2, 1),
(4, '2025-07-02', '14:00:00', '20:00:00', 2, 1),
(5, '2025-07-03', '08:00:00', '14:00:00', 1, 1),
(6, '2025-07-03', '14:00:00', '20:00:00', 1, 1),
(7, '2025-07-04', '08:00:00', '14:00:00', 2, 1),
(8, '2025-07-04', '14:00:00', '20:00:00', 2, 1),
(9, '2025-07-05', '08:00:00', '14:00:00', 1, 1),
(10, '2025-07-05', '14:00:00', '20:00:00', 1, 1),
(11, '2025-07-06', '08:00:00', '14:00:00', 2, 1),
(12, '2025-07-06', '14:00:00', '20:00:00', 2, 1),
(13, '2025-07-07', '08:00:00', '14:00:00', 1, 1),
(14, '2025-07-07', '14:00:00', '20:00:00', 1, 1),
(15, '2025-07-08', '08:00:00', '14:00:00', 2, 1),
(16, '2025-07-08', '14:00:00', '20:00:00', 2, 1),
(17, '2025-07-09', '08:00:00', '14:00:00', 1, 1),
(18, '2025-07-09', '14:00:00', '20:00:00', 1, 1),
(19, '2025-07-10', '08:00:00', '14:00:00', 2, 1),
(20, '2025-07-10', '14:00:00', '20:00:00', 2, 1);

-- ===================================
-- Escalas (20 registros)
-- Note que o nome da tabela muda: escalas -> escala_app_escala
-- Colunas de FK mudam: id_plantao -> plantao_id | id_profissional -> profissional_id
-- STATUS ORIGINAL MANTIDO: 'ativo'
-- ===================================

INSERT INTO escala_app_escala (id, plantao_id, profissional_id, status, data_alocacao) VALUES
(1, 1, 1, 'ativo', '2025-10-01 10:00:00'),
(2, 2, 2, 'ativo', '2025-10-01 10:00:00'),
(3, 3, 3, 'ativo', '2025-10-01 10:00:00'),
(4, 4, 4, 'ativo', '2025-10-01 10:00:00'),
(5, 5, 5, 'ativo', '2025-10-01 10:00:00'),
(6, 6, 6, 'ativo', '2025-10-01 10:00:00'),
(7, 7, 7, 'ativo', '2025-10-01 10:00:00'),
(8, 8, 8, 'ativo', '2025-10-01 10:00:00'),
(9, 9, 9, 'ativo', '2025-10-01 10:00:00'),
(10, 10, 10, 'ativo', '2025-10-01 10:00:00'),
(11, 11, 11, 'ativo', '2025-10-01 10:00:00'),
(12, 12, 12, 'ativo', '2025-10-01 10:00:00'),
(13, 13, 13, 'ativo', '2025-10-01 10:00:00'),
(14, 14, 14, 'ativo', '2025-10-01 10:00:00'),
(15, 15, 15, 'ativo', '2025-10-01 10:00:00'),
(16, 16, 16, 'ativo', '2025-10-01 10:00:00'),
(17, 17, 17, 'ativo', '2025-10-01 10:00:00'),
(18, 18, 18, 'ativo', '2025-10-01 10:00:00'),
(19, 19, 19, 'ativo', '2025-10-01 10:00:00'),
(20, 20, 20, 'ativo', '2025-10-01 10:00:00');

-- ===================================
-- Substituições (7 registros)
-- Note que o nome da tabela muda: substituicoes -> escala_app_substituicao
-- Colunas de FK mudam: id_escala_original -> escala_original_id, etc.
-- STATUS ORIGINAL MANTIDO: 'pendente' ou 'aprovado'
-- Adicionado campo 'aprovada_por_supervisor' (False=0, True=1)
-- ===================================

INSERT INTO escala_app_substituicao (id, escala_original_id, profissional_solicitante_id, profissional_substituto_id, status, data_solicitacao, aprovada_por_supervisor) VALUES
(1, 2, 2, 4, 'pendente', '2025-10-01 10:00:00', 0), 
(2, 3, 3, 5, 'aprovado', '2025-10-01 10:00:00', 1),
(3, 4, 4, 6, 'pendente', '2025-10-01 10:00:00', 0),
(4, 5, 5, 7, 'pendente', '2025-10-01 10:00:00', 0),
(5, 6, 6, 8, 'aprovado', '2025-10-01 10:00:00', 1),
(6, 7, 7, 9, 'pendente', '2025-10-01 10:00:00', 0),
(7, 8, 8, 10, 'aprovado', '2025-10-01 10:00:00', 1);

-- ===================================
-- Auditoria (15 registros)
-- Note que o nome da tabela muda: auditoria -> escala_app_auditoria
-- ===================================

INSERT INTO escala_app_auditoria (id, entidade, id_entidade, acao, usuario, data_hora) VALUES
(1, 'substituicoes', 1, 'criado', 'sistema', '2025-10-01 10:00:00'),
(2, 'substituicoes', 2, 'aprovado', 'supervisor', '2025-10-02 11:00:00'),
(3, 'substituicoes', 3, 'criado', 'sistema', '2025-10-03 12:00:00'),
(4, 'substituicoes', 4, 'criado', 'sistema', '2025-10-03 13:00:00'),
(5, 'substituicoes', 5, 'criado', 'sistema', '2025-10-04 14:00:00'),
(6, 'substituicoes', 6, 'criado', 'sistema', '2025-10-04 15:00:00'),
(7, 'substituicoes', 7, 'aprovado', 'supervisor', '2025-10-05 16:00:00'),
(8, 'escalas', 1, 'criado', 'sistema', '2025-09-30 09:00:00'),
(9, 'escalas', 2, 'criado', 'sistema', '2025-09-30 09:00:00'),
(10, 'escalas', 3, 'criado', 'sistema', '2025-09-30 09:00:00'),
(11, 'escalas', 4, 'criado', 'sistema', '2025-09-30 09:00:00'),
(12, 'escalas', 5, 'criado', 'sistema', '2025-09-30 09:00:00'),
(13, 'escalas', 6, 'criado', 'sistema', '2025-09-30 09:00:00'),
(14, 'escalas', 7, 'criado', 'sistema', '2025-09-30 09:00:00'),
(15, 'escalas', 8, 'criado', 'sistema', '2025-09-30 09:00:00');
