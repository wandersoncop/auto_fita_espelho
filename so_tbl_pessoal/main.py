""" Processa os arquivos da fita espelho e envia os dados para o banco"""

import os  # biblioteca padrão do py serve para interagir com o sistema operacional(caminhos,pasta...)
import pandas as pd  # blibioteca para manipulaçao de dados, como se fosse um excel dentro do py

from sqlalchemy import text  # vai importar os sql ex do tipo 3 que fizemos

from funcoes import (
    ler_fita_por_tipo,  # chama a função que Le o registros fa fita e os separa por tipo
    extrair_tipo_0,  # serve somente para extrair o mes fita
    criar_escolaridade
)

# aqui fazemos os imports dos mapeamento dos campos  que vem la do mapeamento
from mapeamentos import (
    LAYOUT_TIPO_1,
    LAYOUT_TIPO_2,
    HEADER_TIPO_2,
    LAYOUT_TIPO_3,
    CAMPOS_DATA
)

from conexao import engine


# =========================
#  REGRA DE CRIAÇÃO DOS CAMPOS COM BASE NAS TABELAS AUXILIARES
# =========================

# ESTADO CIVIL-----------------------------------------------------------------------------------------------
df_estado_civil = pd.read_sql(
    "SELECT CodECiv, DenoECiv FROM aux_estado_civil",
    engine
)

mapa_estado_civil = dict(
    zip(
        df_estado_civil['CodECiv'],
        df_estado_civil['DenoECiv']
    )
)

# PAIS-------------------------------------------------------------------------------------------
df_pais = pd.read_sql(
    "SELECT CODPAIS, DENOPAIS FROM aux_pais",
    engine
)

mapa_pais = dict(
    zip(
        df_pais['CODPAIS'],
        df_pais['DENOPAIS']
    )
)

# DenoEscolaridade-----------------------------------------------------------------------------
df_escolaridade = pd.read_sql(
    "SELECT CodEsco, DenoEscol FROM aux_escolaridade",
    engine
)

mapa_escolaridade = dict(
    zip(
        df_escolaridade['CodEsco'],
        df_escolaridade['DenoEscol']
    )
)

# DenoTitulacao----------------------------------------------------------------------------------
df_titulacao = pd.read_sql(
    "SELECT CodTit, DenoTit FROM aux_titulacao",
    engine
)

mapa_titulacao = dict(
    zip(
        df_titulacao['CodTit'],
        df_titulacao['DenoTit']
    )
)

# Titulacao correcao---------------------------------------------------------------------------
df_titulacao_correcao = pd.read_sql(
    """
    SELECT 
        codEscolaridade,
        codTitulacao,
        denoEscolaridade,
        grauEscolaridade
    FROM aux_titulacao_correcao
    """,
    engine
)

# pescad matricula ufmg------------------------------------------------------------------------
#cria o campo In
df_pescad_matricula_ufmg = pd.read_sql(
    """
    SELECT
       Inscr,
       SIAPE
    FROM aux_pescad_insc_ufmg   
    """,
    engine
)

mapa_insc_ufmg = dict(
    zip(
        df_pescad_matricula_ufmg['SIAPE'],
        df_pescad_matricula_ufmg['Inscr']
    )
)
# situação------------------------------------------------------------------------
df_situacao = pd.read_sql(
    """
    SELECT 
        CodSit,
        DenoSit
    FROM aux_situacao    

    """,
    engine
)
mapa_situacao = dict(
    zip(
        df_situacao['CodSit'],
        df_situacao['DenoSit']

    )
)
# deno cargo------------------------------------------------------------------------
df_deno_cargo = pd.read_sql(
    """
    SELECT
        GRCARGO,
        CARGO,
        NOME_CARGO
    FROM aux_cargo    
    """,
    engine
)
mapa_deno_cargo = dict(
    zip(
        df_deno_cargo['GRCARGO'].astype(str).str.zfill(3) 
        + df_deno_cargo['CARGO'].astype(str).str.zfill(3),
        df_deno_cargo['NOME_CARGO'] 
    )
)

df_classe = pd.read_sql(
    """
    SELECT
        ChaveClasse,
        DenoClasse
    FROM aux_classe    
    """,
    engine
)
mapa_classe = dict(
    zip(
        df_classe['ChaveClasse'],
        df_classe['DenoClasse'],
    )
)
# unid lotação------------------------------------------------------------------------

df_unidade = pd.read_sql(
    """
    SELECT
        CodUnid,
        Unid,
        DenoSetor,
        UorgPai,
        NomeUorgPai
    FROM aux_unidade_atual   
    """,
    engine
)
df_unidade = df_unidade.drop_duplicates(
    subset=['CodUnid'],
    keep='first'
)
mapa_unidade = (
    df_unidade.set_index('CodUnid')
    [['Unid','DenoSetor','UorgPai','NomeUorgPai']]
    .to_dict('index')
)
df_email_uorg = pd.read_sql(
    """
    SELECT
        UORGSiape,
        `ED-EMAIL-UORG`,
        `NO-MUNICIPIO-END-UORG`,
        `SG-UF-END-UORG`
    FROM aux_uorg_endereco
    """,
    engine
)
mapa_email_uorg = (
    df_email_uorg
    .drop_duplicates(subset=['UORGSiape'], keep='first')
    .set_index('UORGSiape')
    [['ED-EMAIL-UORG', 'NO-MUNICIPIO-END-UORG', 'SG-UF-END-UORG']]
    .to_dict('index')
)
df_municipio = pd.read_sql(
    """
    SELECT
        CODMUNICIP,
        DENOMUNIC
    FROM aux_municipio
    """,
    engine
)

mapa_municipio = dict(
    zip(
        df_municipio['CODMUNICIP'],
        df_municipio['DENOMUNIC']
    )
)
df_local_ap = pd.read_sql(
    """
    SELECT
        MATRIC,
        NrUorgLocalAp,
        DenoSetorLocalAp
        
    FROM aux_local_aposentadoria
    """,
    engine
)
mapa_local_ap = (
   df_local_ap
   .drop_duplicates(subset=['MATRIC'],keep='first')
   .set_index('MATRIC')
   [['NrUorgLocalAp','DenoSetorLocalAp']]
   .to_dict('index')

)

df_atividade = pd.read_sql(
    """
    SELECT
        CODATIV,
        DENOATIV
    FROM aux_atividade
    """,
    engine
)
mapa_atividade = dict(
    zip(
        df_atividade['CODATIV'],
        df_atividade['DENOATIV']
    )
)

# =========================
# CAMINHOS
# =========================

diretorio = os.path.join(
    os.path.expanduser("~"),
    "Desktop",
    "auto_fita_espelho"
)  # retorna a pasta do usuario logado

ARQUIVO = 'fita_espelho.txt'  # arquivo que será traduzido

caminho_arquivo = os.path.join(diretorio, ARQUIVO)


# =========================
# PROCESSAMENTO
# =========================

if os.path.exists(caminho_arquivo):

    print("✅ Arquivo encontrado:")

    # aqui é cria  todos os campos com bse nas regras que vem dos mapas tbl auxiliares 
    mapas_auxiliares = {
        'CodEstadoCiv': {
            'nome_campo': 'EstadoCiv',
            'mapa': mapa_estado_civil
        },
        'CodPais': {
            'nome_campo': 'Pais',
            'mapa': mapa_pais
        },
        'CodEscolaridade': {
            'nome_campo': 'DenoEscolaridade',
            'mapa': mapa_escolaridade
        },
        'CodTitulacao': {
            'nome_campo': 'DenoTitulacao',
            'mapa': mapa_titulacao
        },
        'SIAPE': {
            'nome_campo': 'InscUFMG',
            'mapa': mapa_insc_ufmg
        },
        'CodSituacao':{#nome do campo referencia no header
            'nome_campo':'Situacao',
            'mapa':mapa_situacao
        },
        'CodCargo':{
            'nome_campo': 'DenoCargo',
            'mapa':mapa_deno_cargo
        },
        'ChaveClass': {
            'nome_campo': 'DenoClasse',
            'mapa': mapa_classe
        },
        'CodFunc':{
            'nome_campo':'DenoAtiv',
            'mapa':mapa_atividade
        }
        

    }

    # =========================
    # TIPO 0 - mes_fita
    # =========================

    # aqui extrai o mes fita
    mes_fita = extrair_tipo_0(caminho_arquivo)

    print(f'📅 Mês da fita: {mes_fita}')

    # =========================
    # TIPO 1 - PESSOAL
    # =========================
    #extração e estruturação dos dados
    registros_tipo_1 = ler_fita_por_tipo(
        caminho_arquivo,# onde esta o arquivo
        LAYOUT_TIPO_1,# mapeamento
        '1',#tipo do arquivo ex:tipo_1,tipo_2,tipo_3....
        CAMPOS_DATA,#lista de campos que são data
        mapas_auxiliares, # e o dicionario para configuracao dos novos campos
    )

    print(f'Tipo_1_pessoal finalizado: {len(registros_tipo_1)} registros') #exibe mensagem com quantidade de registros encontrados

    df_pessoal = pd.DataFrame(registros_tipo_1)

    # insere o mes fita na tbl
    df_pessoal.insert(
        0,
        'mes_fita',
        mes_fita
    )
    # =========================
    # TIPO 2 - FUNCIONAL
    # =========================
    registros_tipo_2 = ler_fita_por_tipo(
        caminho_arquivo, #onde esta o arquivo
        LAYOUT_TIPO_2, #chama o mapeamento da fita
        '2',#tipo do arquivo
        CAMPOS_DATA,#busca os campos que são data
        mapas_auxiliares,
    )
    print(f'Tipo_2_funcional finalizado: {len(registros_tipo_2)} registros')#exibe mensagem com quantidade de registros encontrados

    df_funcional = pd.DataFrame(registros_tipo_2)# cria como se fosse um excel na memoria

    #--------------------------------- CRIA A COLUNA 
    df_funcional['UnidLotacao']= df_funcional['NrUorgLotacao'].apply(
        lambda codigo: mapa_unidade.get(codigo,{}).get('Unid','')
    )
    df_funcional['DenoSetorLotacao'] = df_funcional['NrUorgLotacao'].apply(
        lambda codigo:mapa_unidade.get(codigo,{}).get('DenoSetor','')
    )
    df_funcional['UorgPaiExercicio'] = df_funcional['NrUorgLotacao'].apply(
        lambda  codigo:mapa_unidade.get(codigo,{}).get('UorgPai','')
    )
    df_funcional['NomeUorgPaiExercicio'] = df_funcional['NrUorgLotacao'].apply(
        lambda codigo: mapa_unidade.get(codigo,{}).get('NomeUorgPai','')
    )
    df_funcional['FuncSetor'] = df_funcional.apply(
        lambda linha: linha['NOVFUNCUNORG']
        if linha['NOVFUNCSIGLA'] != '' and linha['NOVFUNCUNORG'] != '000000000'
        else linha['FUNCUNORG'],
        axis=1
    )
    df_funcional['NrUorgExercicio'] = df_funcional.apply(
        lambda linha:
            linha['FuncSetor']
            if str(linha['FuncSetor']).strip() not in ('', '000000000')
            else linha['NrUorgLotacao'],
        axis=1
    )
    
    df_funcional['UnidExercicio'] = df_funcional['NrUorgExercicio'].apply(
        lambda codigo:mapa_unidade.get(codigo,{}).get('Unid','')
    )
    df_funcional['DenoSetorExercicio'] = df_funcional['NrUorgExercicio'].apply(
        lambda codigo:mapa_unidade.get(codigo,{}).get('DenoSetor','')
    )
    df_funcional['EmailUORGExercicio'] = df_funcional['NrUorgExercicio'].apply(
    lambda codigo: mapa_email_uorg.get(codigo, {}).get('ED-EMAIL-UORG', '')
    )
    df_funcional['CodMunicipioUORGExercicio'] = df_funcional['NrUorgExercicio'].apply(
        lambda codigo: mapa_email_uorg.get(codigo, {}).get('ED-MUNICIPIO-ENDERECO-UORG', '')
    )
    df_funcional['MunicipioUORGExercicio'] = df_funcional['CodMunicipioUORGExercicio'].apply(
    lambda codigo: mapa_municipio.get(codigo, '')
    )
    df_funcional['NrUorgLocalAp'] = df_funcional['SIAPE'].apply(
    lambda siape: mapa_local_ap.get(str(siape).zfill(7), {}).get('NrUorgLocalAp', '')
    )
    df_funcional['DenoSetorLocalAp'] = df_funcional['SIAPE'].apply(
        lambda siape: mapa_local_ap.get(str(siape).zfill(7), {}).get('DenoSetorLocalAp', '')
    )
    df_funcional['UnidFuncao'] = df_funcional['FUNCUNORG'].apply(
    lambda codigo: mapa_unidade.get(codigo, {}).get('Unid', '')
    )
    df_funcional['DenoSetorFunc'] = df_funcional['FUNCUNORG'].apply(
    lambda codigo: mapa_unidade.get(codigo, {}).get('DenoSetor', '')
    )
    df_funcional['DenoAtiv'] = df_funcional['CodFuncao'].apply(
    lambda codigo: mapa_atividade.get(codigo, '')
    )
    



#-----------------------CRIA A COLUNA E ESTABELECE REGRAS DE NEGOCIO DE CATEGORIA
    df_funcional['Categoria'] = df_funcional['GrCargo'].apply(
    lambda gr_cargo: 'Docente'
    if gr_cargo in ('060', '702', '705', '706', '707')
    else 'Tec-Administrativo'
    )
#-----------------------CRIA A COLUNA E ESTABELECE REGRAS DE NEGOCIO DO TEM FUNCAO   
    df_funcional['TemFuncao'] = df_funcional.apply(
    lambda linha: 'S'
    if (
        str(linha.get('GrExclusao', '')).strip() in ('00', '0')
        and str(linha.get('CodSituacao', '')).strip() != '02'
        and str(linha.get('Funcao', '')).strip() != ''
        and str(linha.get('Funcao', '')).strip() != 'ETG'
        and str(linha.get('DataChefFim', '')).strip() in ('00000000', '00/00/0000', '')
    )
    else 'N',
    axis=1
)

    df_funcional = df_funcional.merge( #busca o campo Nome da tabela pessoal e coloca na ultima posicao
        df_pessoal[['SIAPE','Nome']],
        on= 'SIAPE',
        how='left'
    )
    
    nome_coluna = df_funcional.pop('Nome')# remove a coluna da ultima posicao para reinserir na posição indicada

    posicao = df_funcional.columns.get_loc('SiapeDig') + 1 #aqui indica onde colocar o campo apos SiapeDig

    df_funcional.insert(# aqui inserre de fato o campo na posição
        posicao,
        'Nome',
        nome_coluna
    )

    df_funcional.insert(# faz a inserção do campo mes_fita na tbl funcional
        0,#posição 1 coluna
        'mes_fita', #nome da coluna
         mes_fita #valor da coluna
    )


  

    df_funcional = df_funcional[HEADER_TIPO_2]

    df_funcional.to_csv(#cria o csv
        'tipo_2_funcional.csv',
        sep=';',
        index=False,
        encoding='utf-8-sig'

    )
    # aqui envia para o banco com o .to_sql
    df_funcional.to_sql(
        'tbl_funcional',
        engine,
        if_exists='replace',
        index=False
    )

    print("✅ tipo_2_funcional salvo no banco!")


    # =========================
    # TIPO 3 - PAGAMENTO
    # =========================

    registros_tipo_3 = ler_fita_por_tipo(
        caminho_arquivo,
        LAYOUT_TIPO_3,
        '3',
        CAMPOS_DATA,
        mapas_auxiliares=None
    )

    print(f'Tipo_3_registro_pagamento finalizado: {len(registros_tipo_3)} registros')

    df_pagamento = pd.DataFrame(registros_tipo_3)

    df_pagamento.insert(
        0,  # primeira coluna
        'mes_fita',  # nome da coluna
        mes_fita  # valor
    )

    df_pagamento.to_csv(
        'tipo_3_registro_pagamento.csv',
        sep=';',
        index=False,
        encoding='utf-8-sig'
    )

    print("✅ CSV tipo_3_registro_pagamento.csv exportado com sucesso!")

    # aqui envia para o banco com o .to_sql
    df_pagamento.to_sql(
        'tbl_registro_pagamento',
        engine,
        if_exists='replace',
        index=False
    )

    print("✅ tipo_3_registro_pagamento salvo no banco!")

    # =========================
    # CRIAÇÃO DE TABELA tbl_pgto_incentivo_qualificacao
    # =========================

    query_drop = """
    DROP TABLE IF EXISTS tbl_pgto_incentivo_qualificacao;
    """

    query_create = """
    CREATE TABLE tbl_pgto_incentivo_qualificacao AS
    SELECT
        rp.SIAPE,
        rp.CodRub,
        rp.Seq,
        rp.Valor,
        riq.DENOQUALIF,
        riq.PERQUALIF
    FROM tbl_registro_pagamento rp
    INNER JOIN aux_rubrica_incentivo_qualificacao riq
        ON rp.CodRub = riq.CODQUALIF;
    """

    with engine.begin() as conexao:
        conexao.execute(text(query_drop))
        conexao.execute(text(query_create))

    print("✅ tbl_pgto_incentivo_qualificacao criada com sucesso!")

    # =========================
    # MAPA PERQUALIF
    # =========================

    df_perqualif = pd.read_sql(
        """
        SELECT
            SIAPE,
            MAX(PERQUALIF) AS PERQUALIF
        FROM tbl_pgto_incentivo_qualificacao
        GROUP BY SIAPE
        """,
        engine
    )

    mapa_perqualif = dict(
        zip(
            df_perqualif['SIAPE'],
            df_perqualif['PERQUALIF']
        )
    )

    # =========================
    # ESCOLARIDADE FINAL
    # =========================

    df_pessoal = criar_escolaridade(
        df_pessoal,
        df_titulacao_correcao,
        mapa_perqualif
    )

    print("✅ Campo Escolaridade criado com sucesso!")

    # =========================
    # SALVA TIPO 1
    # =========================

    df_pessoal.to_csv(
        'tipo_1_pessoal.csv',
        sep=';',
        index=False,  # evita criar coluna extra com index
        encoding='utf-8-sig'
    )

    print("✅ CSV tipo_1_pessoal.csv exportado com sucesso!")

    df_pessoal.to_sql(
        'tbl_pessoal',
        engine,
        if_exists='replace',
        index=False
    )

    print("✅ tipo_1_pessoal salvo no banco!")

else:
    print("❌ Arquivo não encontrado.")