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

    CASE 
        WHEN  p.Sexo = 'M'
        THEN 'Masculino'
        ELSE 'Feminino'
    END AS Sexo,
    
    p.DataNasc,
    p.Mae,
    p.CodEstadoCiv,
    ec.DenoECiv AS EstadoCiv,
    p.CodEscolaridade,
    es.denoEscolaridade AS DenoEscolaridade,
    
    CASE 
    WHEN es.grauEscolaridade IS NOT NULL 
         AND tit.grauEscolaridade IS NOT NULL THEN
        CASE 
            WHEN CAST(es.grauEscolaridade AS SIGNED) 
                 >= CAST(tit.grauEscolaridade AS SIGNED)
                THEN es.denoEscolaridade

            ELSE tit.denoEscolaridade 
        END

        -- 2. Se houver apenas Titulação válida
        WHEN tit.grauEscolaridade IS NOT NULL THEN
            tit.denoEscolaridade

        -- 3. Se houver apenas Escolaridade válida
        WHEN es.grauEscolaridade IS NOT NULL THEN
            es.denoEscolaridade

        -- 4. Se não houver titulação válida,
        -- tenta descobrir pelo incentivo PERQUALIF
        WHEN (
            p.CodTitulacao IS NULL 
            OR p.CodTitulacao = '00' 
            OR p.CodTitulacao = ''
        ) THEN
            CASE 
                WHEN riq.PERQUALIF IN (52, 50, 35) 
                    THEN 'MESTRADO'

                WHEN riq.PERQUALIF = 75 
                    THEN 'DOUTORADO'

                WHEN riq.PERQUALIF = 30 
                    THEN 'ESPECIALIZACAO NIVEL SUPERIOR'

                ELSE es.denoEscolaridade
            END

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

LEFT JOIN aux_estado_civil ec 
    ON p.CodEstadoCiv = ec.CodECiv

LEFT JOIN aux_pais pa 
    ON p.CodPais = pa.CodPais

LEFT JOIN aux_titulacao_correcao es 
    ON p.CodEscolaridade = es.codEscolaridade

LEFT JOIN aux_titulacao at 
    ON p.CodTitulacao = at.CodTit

LEFT JOIN aux_titulacao_correcao tit 
    ON p.CodTitulacao = tit.codTitulacao

/* JUNÇÃO COM REGISTRO DE PAGAMENTO */
LEFT JOIN (
    SELECT 
        rg_sub.SIAPE, 
        MAX(riq_sub.PERQUALIF) AS PERQUALIF

    FROM tipo_3_rg_pagamento rg_sub

    INNER JOIN aux_rubrica_incentivo_qualificacao riq_sub 
        ON rg_sub.CodRub = riq_sub.CODQUALIF

    GROUP BY rg_sub.SIAPE

) AS riq 
    ON p.SIAPE = riq.SIAPE;
"""
# ---------------------------------------------------------------------------------------
CRIA_TBL_FUNCIONAL = """
DROP TABLE IF EXISTS tbl_funcional;

CREATE TABLE tbl_funcional AS
SELECT
    fc.SIAPE
  
    
   
FROM tipo_2_funcional fc;
"""



# ---------------------------------------------------------------------------------------



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