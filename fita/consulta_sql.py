from sqlalchemy import text

CRIA_TBL_PESSOAL = """
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
    p.CodEscolaridade,
    es.denoEscolaridade AS DenoEscolaridade,

    /* LÓGICA DE ESCOLARIDADE (Fiel à sua função Python + Regra de Rubrica) */
    CASE 
        -- 1. Se ambos os graus existem, compara qual é o maior (Igual ao seu Python)
        WHEN es.grauEscolaridade IS NOT NULL AND tit.grauEscolaridade IS NOT NULL THEN
            CASE 
                WHEN es.grauEscolaridade >= tit.grauEscolaridade THEN es.denoEscolaridade
                ELSE tit.denoEscolaridade 
            END

        -- 2. Se o cadastro de Titulação (TITFORM) estiver vazio ou '00', decide pelo PERQUALIF
        WHEN (p.CodTitulacao IS NULL OR p.CodTitulacao = '00' OR p.CodTitulacao = '') THEN
            CASE 
                WHEN riq.PERQUALIF IN (52, 50, 35) THEN 'MESTRADO'
                WHEN riq.PERQUALIF = 75 THEN 'DOUTORADO'
                WHEN riq.PERQUALIF = 30 THEN 'ESPECIALIZACAO NIVEL SUPERIOR'
                ELSE es.denoEscolaridade 
            END

        -- 3. Se houver apenas Titulação válida no cadastro
        WHEN tit.grauEscolaridade IS NOT NULL THEN tit.denoEscolaridade

        -- 4. Se houver apenas Escolaridade válida no cadastro
        WHEN es.grauEscolaridade IS NOT NULL THEN es.denoEscolaridade

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
LEFT JOIN aux_titulacao_correcao es ON p.CodEscolaridade = es.codEscolaridade
LEFT JOIN aux_titulacao at ON p.CodTitulacao = at.CodTit
LEFT JOIN aux_titulacao_correcao tit ON p.CodTitulacao = tit.codTitulacao

/* JUNÇÃO COM REGISTRO DE PAGAMENTO (Filtrado por SIAPE para evitar duplicados) */
LEFT JOIN (
    SELECT 
        rg_sub.SIAPE, 
        MAX(riq_sub.PERQUALIF) AS PERQUALIF
    FROM tipo_3_rg_pagamento rg_sub
    INNER JOIN aux_rubrica_incentivo_qualificacao riq_sub 
        ON rg_sub.CodRub = riq_sub.CODQUALIF
    GROUP BY rg_sub.SIAPE
) AS riq ON p.SIAPE = riq.SIAPE;
"""

CRIA_TBL_REGISTRO_PAGAMENTO = """
DROP TABLE IF EXISTS tbl_registro_pagamento;

CREATE TABLE tbl_registro_pagamento AS
SELECT
    rg.UnidPag,
    rg.SIAPE,
    rg.SiapeDig,
    rg.TipoReg,
    rg.RendDesc,
    rg.CodRub,
    rg.Seq,
    rg.Valor,
    rg.Prazo,
    rg.Perc,
    rg.Numer,
    rg.Denom,
    rg.AssCalc,
    rg.Sist,
    rg.NivSal,
    rg.PANome,
    rg.PABanco,
    rg.PAAgen,
    rg.PAConta,
    rg.PAAnoMesRub
FROM tipo_3_rg_pagamento rg;
"""

QUERY_LIMPEZA_TEMPORARIOS = """
DROP TABLE IF EXISTS tipo_1_pessoal;
DROP TABLE IF EXISTS tipo_3_rg_pagamento;
"""