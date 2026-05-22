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
        WHEN p.Sexo = 'M' THEN 'Masculino'
        ELSE 'Feminino'
    END AS Sexo,
    
    p.DataNasc,
    p.Mae,
    p.CodEstadoCiv,
    ec.DenoECiv AS EstadoCiv,

    p.CodEscolaridade,
    esc.DenoEscol AS DenoEscolaridade,
    
    CASE 
        WHEN es.codEscolaridade IS NOT NULL 
         AND tit.codTitulacao IS NOT NULL
        THEN
            CASE 
                WHEN CAST(es.grauEscolaridade AS SIGNED) >
                     CAST(tit.grauEscolaridade AS SIGNED)
                THEN es.denoEscolaridade
                ELSE tit.denoEscolaridade
            END

        WHEN p.CodTitulacao IS NULL 
          OR p.CodTitulacao = '00'
          OR p.CodTitulacao = ''
        THEN
            CASE 
                WHEN riq.PERQUALIF IN (52, 50, 35) 
                    THEN 'MESTRADO'
                WHEN riq.PERQUALIF = 75 
                    THEN 'DOUTORADO'
                WHEN riq.PERQUALIF = 30 
                    THEN 'ESPECIALIZACAO NIVEL SUPERIOR'
                ELSE esc.DenoEscol
            END

        ELSE esc.DenoEscol
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

LEFT JOIN aux_escolaridade esc
    ON p.CodEscolaridade = esc.CodEsco

LEFT JOIN aux_titulacao_correcao es 
    ON p.CodEscolaridade = es.codEscolaridade

LEFT JOIN aux_titulacao at 
    ON p.CodTitulacao = at.CodTit

LEFT JOIN aux_titulacao_correcao tit 
    ON p.CodTitulacao = tit.codTitulacao

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
    f.mes_fita,
    f.InscUFMG,
    f.SIAPE,
    f.SiapeDig,
    f.Nome,
    f.RegJuridico,
    f.CodSituacao,
    # f.Situacao,
    # f.Categoria,
    # f.CodRegTrab,
    # f.RegTrabalho,
    f.ANUE,
    f.NumApos,
    f.DenoApos,
    f.GrCargo,
    f.Cargo,
    f.CodCargo,
    f.DenoCargo,
    f.Classe,
    f.DenoClasse,
    f.Referencia,
    f.Setor,
    f.NrUorgLotacao,
    f.UnidLotacao,
    f.DenoSetorLotacao,
    f.NrUorgExercicio,
    f.UnidExercicio,
    f.DenoSetorExercicio,
    # f.MunicipUorgExercicio,
    # f.EmailUorgExercicio,
    f.UorgPaiExercicio,
    f.NomeUorgPaiExercicio,
    f.NrUorgLocalAP,
    f.DenoSetorLocalAp,
    f.GrExclusao,
    f.DataIngOrg,
    f.DataIngSP,
    f.DataExclusao,
    f.DataAposentadoria,
    f.DataObito,
    f.Funcao,
    f.FuncaoNivel,
    f.DataChefInic,
    f.DataChefFim,
    f.TemFuncao,
    # f.FuncaoSetor,
    f.UnidFuncao,
    f.DenoSetorFunc,
    f.FuncaoEsc,
    f.FuncaoOpcao,
    f.NovaFuncEsc,
    f.NovaFuncOpcao,
    f.CodFuncao,
    # f.DenoAtividade,
    f.GrOcorrAposent,
    f.OcorrAposent,
    f.DenoAposent,
    f.GrOcorrIngOrg,
    f.OcorrIngOrg,
    f.DenoIngOrgao,
    f.GrOcorrIngSp,
    f.OcorrIngSp,
   f.DenoIngSerPublico,    
   f.OcorrExclusao, 
   f.DenoExclusao,   
   f.SuspPag,  
   f.DtSusp,    
   f.DtLotacao,
   f.DtCadastro, 
   f.DtOcup,
   f.DtSaida, 
   f.ApoNumProc,
   f.ApoAnoprev,
   f.CtNum,    
   f.CtSer,   
   f.CtUf,
   f.BANCO,
   f.AGENCIA,
   f.CONTA,
   f.AP_OP_INTG,
   f.AposUorg,
   f.OrgDest,
   f.DtLiber,
   f.OrgOrigem,
   f.DenoOrigem,
   f.OrgAnt,
   f.DenoOrgAnt,
   f.SIAPEAnt,
   f.OrgExtMod,
   f.MatServExt,
   f.OrgAtual,
   f.SIAPEAtual,
   f.MudUpagCod,
   f.MudUpagDtLb,
   f.MudUpagMoti,
   f.IPagServ,
   f.ObitoCart,
   f.ObitoLivro,
   f.ObitoFolha,
   f.ObitoReg,    
   f.IExcInsti,
   f.DtExcInti,
   f.VAlimTipo,
   f.VAlimDtIni,
   f.VAlimDtFim,
   f.RX,
   f.OrgReq,
   f.DenoOrgRequisitante,
   f.CodVaga,
   f.ANUEMES,
   f.RxPerc,
   f.GOcorreVat,
   f.OcreverAti,
   f.IndiceCargo,
   f.IndiceFuncao,
   f.IndiceSalarioFamilia,
   f.IndiceAnuenio,
   f.IndiceFGTS,
   f.IndicePSS,
   f.IndiceIR,
   f.IndiceMargemConsig,
   f.indideSindical,
   f.IndiceAdiantamento13,
   f.IndiceAbateTeto,
   f.Indice13Salario,
   f.IndicePSS6,
   f.IndiceFerias,
   f.IndicePensao,
   f.IndiceBeneficio,
   f.IndiceIpmfCpm,
   f.IndiceRais,
   f.IndiceDifURV,
   f.IndiceAdiantamento,
   f.IndicePasep  
    
   
FROM tipo_2_funcional f;
"""



# ---------------------------------------------------------------------------------------



CRIA_TBL_REGISTRO_PAGAMENTO = """
DROP TABLE IF EXISTS tbl_registro_pagamento;

CREATE TABLE tbl_registro_pagamento AS
SELECT
    rp.UnidPag,
    rp.SIAPE,
    rp.SiapeDig,
    rp.TipoReg,
    rp.RendDesc,
    rp.CodRub,
    rp.Seq,
    rp.Valor,
    rp.Prazo,
    rp.Perc,
    rp.Numer,
    rp.Denom,
    rp.AssCalc,
    rp.Sist,
    rp.NivSal,
    rp.PANome,
    rp.PABanco,
    rp.PAAgen,
    rp.PAConta,
    rp.PAAnoMesRub
FROM tipo_3_rg_pagamento rp;
"""

QUERY_LIMPEZA_TEMPORARIOS = """
DROP TABLE IF EXISTS tipo_1_pessoal;
DROP TABLE IF EXISTS tipo_3_rg_pagamento;
"""