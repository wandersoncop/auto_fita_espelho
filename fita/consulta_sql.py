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
    # p.DENO_ESCOL,
    p.ESCOLARIDADE,
p.CodTitulacao,
    # p.DENO_TIT,

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
    ON p.CODPAIS = pa.CodPais
;
"""

QUERY_LIMPEZA_TEMPORARIOS = "DROP TABLE IF EXISTS tipo_1_pessoal;"