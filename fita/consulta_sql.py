# Concentre todas as queries aqui



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

    p.CodTitulacao,
    at.DenoTit AS DenoTitulacao,

    CASE

        -- compara escolaridade x titulação
        WHEN es.grauEscolaridade IS NOT NULL
         AND tit.grauEscolaridade IS NOT NULL
        THEN
            CASE
                WHEN es.grauEscolaridade > tit.grauEscolaridade
                    THEN es.denoEscolaridade

                ELSE tit.denoEscolaridade
            END

        /*
        ============================================================
        REGRA PERQUALIF
        ============================================================

        ESSA PARTE SERÁ IMPLEMENTADA DEPOIS,
        QUANDO A TABELA QUE POSSUI O CAMPO
        PerQualif FOR ADICIONADA.

        EXEMPLO FUTURO:

        WHEN pq.PerQualif IN (52, 50, 35)
            THEN 'MESTRADO'

        WHEN pq.PerQualif = 75
            THEN 'DOUTORADO'

        WHEN pq.PerQualif = 30
            THEN 'ESPECIALIZACAO NIVEL SUPERIOR'
        */

        ELSE es.denoEscolaridade

    END AS Escolaridade,

    p.CodNaturalidade,

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

-- escolaridade original
LEFT JOIN aux_titulacao_correcao es
    ON p.CodEscol = es.codEscolaridade

LEFT JOIN aux_titulacao at
    ON p.CodTitulacao = at.CodTit

-- titulação convertida em escolaridade
LEFT JOIN aux_titulacao_correcao tit
    ON p.CodTitulacao = tit.codTitulacao
;
"""

QUERY_LIMPEZA_TEMPORARIOS = "DROP TABLE IF EXISTS tipo_1_pessoal;"