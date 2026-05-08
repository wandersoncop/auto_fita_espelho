from conexao import engine

# Concentre todas as queries aqui
QUERY_CONSOLIDACAO_PESSOAL = """
-- Primeiro, mata a tabela antiga para não dar erro de coluna duplicada
DROP TABLE IF EXISTS tb_pessoal_consolidada;

-- Cria a tabela nova
CREATE TABLE tb_pessoal_consolidada AS
SELECT 
    p.*, 
    e.DenoECiv AS DENO_E_CIV
FROM tipo_1_pessoal p
LEFT JOIN estado_civil e ON p.ECiv = e.CodECiv;

-- COMANDO MÁGICO PARA MOVER A COLUNA (Só funciona no MySQL)
-- Isso coloca o DENO_E_CIV logo após o ECiv automaticamente!
ALTER TABLE tb_pessoal_consolidada MODIFY COLUMN DENO_E_CIV TEXT AFTER ECiv;
"""

# QUERY_LIMPEZA_TEMPORARIOS = "DROP TABLE IF EXISTS tipo_1_pessoal;"