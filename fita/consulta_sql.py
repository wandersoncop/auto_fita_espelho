# Concentre todas as queries aqui
from sqlalchemy import create_engine, text



QUERY_CONSOLIDACAO_PESSOAL = """
DROP TABLE IF EXISTS tbl_pessoal;

CREATE TABLE tbl_pessoal AS
SELECT 
    p.mes_fita,
    p.UnidPag,
    p.InscUFMG,
    p.SIAPE,
    p.SiapeDig,
    p.TipoReg,
    p.Nome,
    p.CPF,
    p.PASEP,
    p.Sexo,
    p.DataNasc,
    p.Mae,
    p.CodEstadoCiv,
    ec.DenoECiv AS EstadoCiv,
    p.CodEscol,
    es.denoEscolaridade AS DenoEscolaridade,

    -- CAMPO ESCOLARIDADE CORRIGIDO
    CASE
        -- 1. Comparação de Graus quando ambos existem
        WHEN es.codEscolaridade IS NOT NULL 
             AND tit.codTitulacao IS NOT NULL 
             AND es.grauEscolaridade IS NOT NULL 
             AND tit.grauEscolaridade IS NOT NULL THEN
            CASE 
                WHEN es.grauEscolaridade > tit.grauEscolaridade THEN es.denoEscolaridade
                ELSE tit.denoEscolaridade 
            END

        -- 2. Fallback baseado no PERQUALIF (Tradução Access)
        WHEN (p.TITFORM IS NULL OR p.TITFORM = '00') THEN
            CASE
                WHEN p.PERQUALIF IN (52, 50, 35) THEN 'MESTRADO'
                WHEN p.PERQUALIF = 75 THEN 'DOUTORADO'
                WHEN p.PERQUALIF = 30 THEN 'ESPECIALIZACAO NIVEL SUPERIOR'
                ELSE es.denoEscolaridade
            END

        -- 3. Fallbacks Simples
        WHEN tit.codTitulacao IS NOT NULL THEN tit.denoEscolaridade
        ELSE es.denoEscolaridade
    END AS Escolaridade,

    p.CodTitulacao,
    at.DenoTit AS DenoTitulacao,
    p.CodNaturalidade,
    p.Naturalidade,
    p.CodPais,
    pa.DenoPais AS Pais,
    p.AnoChegada,
    p.DepImpRenda,
    p.Sf,
    p.DataPrimEmprego,
    p.SiapeCad,
    p.Logradouro,
    p.Numero,
    p.Complemento,
    p.Bairro,
    p.Municipio,
    p.CEP,
    p.UF,
    p.Identidade,
    p.OrgaoExpedidor,
    p.DataExpedicao,
    p.UfIdent,
    p.TituloEleitor
FROM tipo_1_pessoal p
LEFT JOIN aux_estado_civil ec ON p.CodEstadoCiv = ec.CodECiv
LEFT JOIN aux_pais pa ON p.CodPais = pa.CodPais
LEFT JOIN aux_titulacao_correcao es ON p.CodEscol = es.codEscolaridade
LEFT JOIN aux_titulacao at ON p.CodTitulacao = at.CodTit
LEFT JOIN aux_titulacao_correcao tit ON p.CodTitulacao = tit.codTitulacao;
"""

QUERY_LIMPEZA_TEMPORARIOS = "DROP TABLE IF EXISTS tipo_1_pessoal;"
