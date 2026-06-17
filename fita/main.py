"""
    Processa os arquivos da fita espelho e envia os 
    dados para o banco
"""

import os
# biblioteca padrão do py serve para interagir com 
# o sistema operacional(caminhos,pasta...)
import pandas as pd  # blibioteca para manipulaçao de dados, como se fosse um excel dentro do py

# from conexao_access import conectar_access
# from envia_access import enviar_dataframe_para_access
from sqlalchemy import text  
# Biblioteca para trabalhar com banco de dados.
# O text() faz o SQLAlchemy reconhecer o texto como um comando SQL.

from funcoes import (
    ler_fita_por_tipo,  # chama a função que Le o registros da fita e os separa por tipo
    extrair_tipo_0,  # serve somente para extrair o mes fita
    criar_escolaridade, #Cria o campo Escolaridade comparando escolaridade e titulação
    formatar_valores, # converte em valores
    salvar_dataframe #cria e envia os df paa o banco de dados
)
# from envia_access import enviar_dataframe_para_access

from mapeamentos import (
    # LAYOUT_TIPO_ são as posições na fita ex:'SIAPE': (9, 16),
    # HEADER_TIPO_ faz a sequecia desejada
    # CAMPOS_DATA aqui é  lista de campos de data que serão formatados pela função formatar_data
    LAYOUT_TIPO_1,
    HEADER_TIPO_1,
    LAYOUT_TIPO_2,
    HEADER_TIPO_2,
    LAYOUT_TIPO_3,
    LAYOUT_TIPO_4,
    HEADER_TIPO_4,
    LAYOUT_TIPO_5,
    HEADER_TIPO_5,
    LAYOUT_TIPO_6,
    HEADER_TIPO_6,
    CAMPOS_DATA 
)
from conexao import engine
# Importa o objeto de conexão (engine) utilizado para acessar o banco de dados MySQL.
# conexao_access = conectar_access()
# cursor_access = conexao_access.cursor()

# =========================
# CAMINHOS PARA LOCALIZAÇÃO DE ARQUIVOS
# =========================

diretorio = os.path.join(
    os.path.expanduser("~"),
    "Desktop",
    "auto_fita_espelho",
    "arquivos_fita"
)  # retorna a pasta do usuario logado
print(diretorio)




# ARQUIVO = 'fita_espelho.txt'  # arquivo que será traduzido

# caminho_arquivo = os.path.join(diretorio, ARQUIVO)

# ==============================================
# LOCALIZA O ARQUIVO
# ==============================================

arquivo_encontrado = None

# procura dentro do diretorio um arquivo
# com o nome começando com fita_servidor_
# e com extenção .txt
for arquivo in os.listdir(diretorio):
# lower() coloca tudo em minusculo
# .startswith('começa com')
# .endswith('termina com')
# break para de procurar assim que encontra
    if (
        arquivo.lower().startswith('fita_servidor_')
        and arquivo.lower().endswith('.txt')
    ):
        arquivo_encontrado = arquivo
        break

if arquivo_encontrado:
    caminho_arquivo = os.path.join(
        diretorio,
        arquivo_encontrado
    )
# aqui retorna o arquivo encontrado    # 
else:
    caminho_arquivo = None

if caminho_arquivo and os.path.exists(caminho_arquivo):
    print(f"✅ Arquivo encontrado: {arquivo_encontrado}")



# =========================
#  REGRA DE CRIAÇÃO DOS CAMPOS COM BASE NAS TABELAS AUXILIARES
# =========================

# ESTADO CIVIL-----------------------------------------------------------------------------------------------
df_estado_civil = pd.read_sql(
    # função do Pandas que executa o camandao SQL e devolve um dataframe
    #dataframe é uma tabela em memoria      
    #comando sql
    """
        SELECT 
            CodECiv, 
            DenoECiv 
        FROM aux_estado_civil
    """, 
    engine # é a conexao com o bd Mysql
)
mapa_estado_civil = dict(
    zip(
        df_estado_civil['CodECiv'],
        df_estado_civil['DenoECiv']
    )
)
# PAIS-------------------------------------------------------------------------------------------
df_pais = pd.read_sql(
    """
        SELECT 
            CODPAIS, 
            DENOPAIS 
        FROM aux_pais
    """,
    engine
)
mapa_pais = dict(
    zip(
        df_pais['CODPAIS'],
        df_pais['DENOPAIS']
    )
)
# DENO_ESCOLARIDADE-----------------------------------------------------------------------------
df_escolaridade = pd.read_sql(
    """
        SELECT 
            CodEsco, 
            DenoEscol 
        FROM aux_escolaridade
    """,
    engine
)
mapa_escolaridade = dict(
    zip(
        df_escolaridade['CodEsco'],
        df_escolaridade['DenoEscol']
    )
)
# DENO_TITULACAO----------------------------------------------------------------------------------
df_titulacao = pd.read_sql(
    """SELECT 
        CodTit, 
        DenoTit 
    FROM aux_titulacao""",
    engine
)
mapa_titulacao = dict(
    zip(
        df_titulacao['CodTit'],
        df_titulacao['DenoTit']
    )
)
# TITULACAO CORRECAO---------------------------------------------------------------------------
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
# PESCAD MATRICULA UFMG------------------------------------------------------------------------
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
# SITUACAO------------------------------------------------------------------------
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
# DENO CARGO------------------------------------------------------------------------
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
        df_deno_cargo['GRCARGO']
            .astype(str)
            .str.replace('.0', '', regex=False)
            .str.zfill(3)
        +
        df_deno_cargo['CARGO']
            .astype(str)
            .str.replace('.0', '', regex=False)
            .str.zfill(3),

        df_deno_cargo['NOME_CARGO']
    )
)
#CLASSE-------------------------------------------------
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
# UNID LOTACAO------------------------------------------------------------------------
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
# caso o CodUnid esteja duplicado traz somente a 1 registro
df_unidade = df_unidade.drop_duplicates(
    subset=['CodUnid'],
    keep='first'
)
mapa_unidade = (
    df_unidade.set_index('CodUnid')
    [['Unid','DenoSetor','UorgPai','NomeUorgPai']]
    .to_dict('index')
)
# EMAIL------------------------------------------------------------------------
df_email_uorg = pd.read_sql(
    """
        SELECT
            UORGSiape,
            `ED-EMAIL-UORG`,
            `ED-MUNICIPIO-ENDERECO-UORG`,
            `SG-UF-END-UORG`
        FROM aux_uorg_endereco
    """,
    engine
)
mapa_email_uorg = (
    df_email_uorg
    .drop_duplicates(subset=['UORGSiape'], keep='first')
    .set_index('UORGSiape')
    [['ED-EMAIL-UORG', 'ED-MUNICIPIO-ENDERECO-UORG', 'SG-UF-END-UORG']]
    .to_dict('index')
)
# MUNICIPIO------------------------------------------------------------------------
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
# LOCAL APOSENTADORIA---------------------------------------------------------------------
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
# ATIVIDADE---------------------------------------------------------------------------------
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
# MAPA OCORRENCIA----------------------------------------------------------------------------
df_ocorrencia = pd.read_sql(#faz o select na tabela aux
    """
        SELECT
            GROCOR,
            CODOCOR,
            DESC_OCORR           
        FROM aux_ocorrencia
    """,
    engine
)
mapa_ocorrencia = dict(
  zip(
      df_ocorrencia['GROCOR'].astype(str).str.zfill(2)
      + df_ocorrencia['CODOCOR'].astype(str).str.zfill(3),

      df_ocorrencia['DESC_OCORR']
  )
)
# ORGAOS-----------------------------------------------------------------------------------
df_orgaos = pd.read_sql(
   """ 
        SELECT
            COD_ORGAO,
            NOME_ORGAO
        FROM aux_orgaos  
    """,
    engine  
)
mapa_orgaos = dict(
    zip(
        df_orgaos['COD_ORGAO'],
        df_orgaos['NOME_ORGAO']
    )
)
# CAD APF-----------------------------------------------------------------------------------
df_cad_apf = pd.read_sql(
    """
        SELECT
            Mat,
            A0300_carcod,
            A0300_grccod,
            f0300_ctfsgr
        FROM aux_cad_apf
    """,
    engine
)
mapa_cad_apf_cargo = dict(
    zip(
        df_cad_apf['Mat'].astype(str).str.replace('.0', '', regex=False).str.zfill(7),
        df_cad_apf['A0300_carcod'].astype(str).str.replace('.0', '', regex=False).str.zfill(3)
    )
)
mapa_cad_apf_gr_cargo = dict(
    zip(
        df_cad_apf['Mat'].astype(str).str.replace('.0', '', regex=False).str.zfill(7),
        df_cad_apf['A0300_grccod'].astype(str).str.replace('.0', '', regex=False).str.zfill(3)
    )
)
mapa_cad_apf_clas = dict(
    zip(
        df_cad_apf['Mat'].astype(str).str.replace('.0', '', regex=False).str.zfill(7),
        df_cad_apf['f0300_ctfsgr'].astype(str).str.replace('.0', '', regex=False)
    )
)
# RUBRICA-----------------------------------------------------------------------
df_rubrica = pd.read_sql(#faz o select na tabela aux
    """
        SELECT
            Rubrica,
            DescRubri            
        FROM aux_rubrica
    """,
    engine
)
mapa_rubrica = dict(
  zip(
      df_rubrica['Rubrica'].astype(str).str.zfill(5),
      df_rubrica['DescRubri'].astype(str)     
    )
)

# ==============================================================
# PROCESSAMENTO
# ==============================================================

print(diretorio)

if caminho_arquivo and os.path.exists(caminho_arquivo):    

    print(f"✅ Arquivo encontrado:{arquivo_encontrado}")

    # aqui é cria  todos os campos com base nas regras que vem dos mapas tbl auxiliares 
    mapas_auxiliares = {

        'CodEstadoCiv': {              #campo original da fita
            'nome_campo': 'EstadoCiv', # campo novo que será criado após a tradução
            'mapa': mapa_estado_civil  #tabela de conversão usada na tradução
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
        'CodSituacao':{
            'nome_campo':'Situacao',
            'mapa':mapa_situacao
        },       
        'ChaveClass': {
            'nome_campo': 'DenoClasse',
            'mapa': mapa_classe
        },
        'CodRub': { #campo que será traduzido, campo que existe na fita 'LAYOUT_TIPO'
            'nome_campo': 'DenoRubrica',# no dado ao campo que será criado apos a traducao
            'mapa': mapa_rubrica # mapa que será utilizado
        }   
    }
    # ====================================================================
    # TIPO 0 - MesFita
    # ====================================================================
    # AQUI FAREMOS SOMENTE A EXTRACAO DO MES FITA
    MesFita = extrair_tipo_0(caminho_arquivo)
    print(f'📅 Mês da fita: {MesFita}')

    # ====================================================================
    # TIPO 1 - PESSOAL
    # ====================================================================
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
        'MesFita',
        MesFita
    )

    # ====================================================================
    # TIPO 2 - FUNCIONAL
    # ====================================================================
    registros_tipo_2 = ler_fita_por_tipo(
        caminho_arquivo, #onde esta o arquivo
        LAYOUT_TIPO_2, #chama o mapeamento da fita
        '2',#tipo do arquivo
        CAMPOS_DATA,#busca os campos que são data
        mapas_auxiliares,
    )
    print(f'Tipo_2_funcional finalizado: {len(registros_tipo_2)} registros')#exibe mensagem com quantidade de registros encontrados

    df_funcional = pd.DataFrame(registros_tipo_2)# cria como se fosse um excel na memoria

    #--------------------------------- CRIA O CAMPO
    # cria o campo UnidLotacao usando o valor que esta em NrUorgLotacao
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
        lambda linha:
            linha['NOVFUNCUNORG']
            if str(linha.get('NOVFUNCSIGLA', '')).strip() != ''
            else linha['FUNCUNORG'],
        axis=1
    )
    df_funcional['TemFuncao'] = df_funcional.apply(
        lambda linha: 'S'
        if (
            str(linha.get('GrExclusao', '')).strip() in ('00', '0')
            and str(linha.get('CodSituacao', '')).strip() != '02'
            and str(linha.get('Funcao', '')).strip() != ''
            and str(linha.get('Funcao', '')).strip() != 'ETG'
            and str(linha.get('DataFuncFim', '')).strip() in ('', '00000000')
        )
        else 'N',
        axis=1
    )
    df_funcional['NrUorgExercicio'] = df_funcional.apply(
        lambda linha:
            linha['Setor']
            if str(linha.get('RegJuridico', '')).strip() in ('MRD', 'RMP')
            else (
                linha['FuncSetor']
                if (
                    str(linha.get('TemFuncao', '')).strip() == 'S'
                    or (
                        str(linha.get('Funcao', '')).strip() != ''
                        and str(linha.get('NOVFUNCSIGLA', '')).strip() != ''
                        and str(linha.get('NOVFUNCDTSAIDA', '')).strip() == '00000000'
                        and str(linha.get('Setor', '')).strip() == '000000000'
                    )
                )
                else (
                    linha['Setor']
                    if str(linha.get('NrUorgLotacao', '')).strip() == '000000000'
                    else linha['NrUorgLotacao']
                )
            ),
        axis=1
    )
    df_funcional['UnidExercicio'] = df_funcional['NrUorgExercicio'].apply(
        lambda codigo:mapa_unidade.get(codigo,{}).get('Unid','')
    )
    df_funcional['DenoSetorExercicio'] = df_funcional['NrUorgExercicio'].apply(
        lambda codigo:mapa_unidade.get(codigo,{}).get('DenoSetor','')
    )
    df_funcional['EmailUorgExercicio'] = df_funcional['NrUorgExercicio'].apply(
        lambda codigo: mapa_email_uorg.get(codigo, {}).get('ED-EMAIL-UORG', '')
    )
    df_funcional['CodMunicipioUORGExercicio'] = df_funcional['NrUorgExercicio'].apply(
        lambda codigo: mapa_email_uorg.get(codigo, {}).get('ED-MUNICIPIO-ENDERECO-UORG', '')
    )
    df_funcional['MunicipioUorgExercicio'] = df_funcional['CodMunicipioUORGExercicio'].apply(
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
    df_funcional['DenoAposent'] = (# nomes iguai ao do mapeamento que vai ser exibido na tabela
        df_funcional['GrOcorrAposent'].astype(str).str.zfill(2)
        + df_funcional['OcorrAposent'].astype(str).str.zfill(3)
    ).apply(
        lambda codigo:mapa_ocorrencia.get(codigo,'')
    )
    df_funcional['DenoIngOrgao'] = (
        df_funcional['GrOcorrIngOrg'].astype(str).str.zfill(2)
       + df_funcional['OcorrIngOrg'].astype(str).str.zfill(3)
    ).apply(
        lambda codigo:mapa_ocorrencia.get(codigo,'')
    )
    df_funcional['DenoIngSerPublico'] = (
        df_funcional['GrOcorrIngSp'].astype(str).str.zfill(2)
        + df_funcional['OcorrIngSp'].astype(str).str.zfill(3)
    ).apply(
        lambda codigo:mapa_ocorrencia.get(codigo,'')
    )
    df_funcional['DenoExclusao'] = (        
        df_funcional['GrExclusao'].astype(str).str.zfill(2)
        +df_funcional['OcorrExclusao'].astype(str).str.zfill(3)
    ).apply(
        lambda codigo:mapa_ocorrencia.get(codigo,'')
    )    
    df_funcional['DenoOrigem'] = df_funcional['OrgOrigem'].apply(
        lambda codigo:mapa_orgaos.get(codigo,'')
    )
    df_funcional['DenoOrgAnt'] = df_funcional['OrgAnt'].apply(
        lambda codigo: mapa_orgaos.get(codigo,'')
    )
    df_funcional['DenoOrgRequisitante'] = df_funcional['OrgAnt'].apply(
        lambda codigo: mapa_orgaos.get(codigo,'')
    )

#-----------------------CRIA As REGRAS DE NEGOCIO Do CARGO QUE INFLUENCIA NA CATEGORIA MAGISTERIO
     
    df_funcional['GrCargo'] = df_funcional.apply(
    lambda linha:
        mapa_cad_apf_gr_cargo.get(str(linha['SIAPE']).zfill(7))
        if str(linha['CodSituacao']).strip() == '19'
        and mapa_cad_apf_gr_cargo.get(str(linha['SIAPE']).zfill(7)) is not None
        else str(linha['GrCargo']).replace('.0', '').zfill(3),
    axis=1
    )
    df_funcional['Cargo'] = df_funcional.apply(
        lambda linha:
            mapa_cad_apf_cargo.get(str(linha['SIAPE']).zfill(7))
            if str(linha['CodSituacao']).strip() == '19'
            and mapa_cad_apf_cargo.get(str(linha['SIAPE']).zfill(7)) is not None
            else str(linha['CodCargo']).replace('.0', '')[-3:].zfill(3),
        axis=1
    )
    df_funcional['CodCargo'] = df_funcional['GrCargo'] + df_funcional['Cargo']

    df_funcional['DenoCargo'] = df_funcional['CodCargo'].apply(
        lambda codigo: mapa_deno_cargo.get(codigo, '')
    )
#-----------------------CRIA A REGRA DE NEGOCIO DA CLASSE CONFORME ACCESS
    df_funcional['Classe'] = df_funcional.apply(
        lambda linha:
            mapa_cad_apf_clas.get(str(linha['SIAPE']).zfill(7))
            if str(linha['CodSituacao']).strip() == '19'
            and mapa_cad_apf_clas.get(str(linha['SIAPE']).zfill(7)) is not None
            else str(linha['Classe']).replace('.0', '').strip(),
        axis=1
    )
#-----------------------CRIA A COLUNA E ESTABELECE REGRAS DE NEGOCIO DE CATEGORIA
    df_funcional['Categoria'] = df_funcional['GrCargo'].apply(
        lambda gr_cargo: 'Docente'
        if str(gr_cargo).strip().zfill(3) in ('060', '702', '705', '706', '707')
        else 'Tec-Administrativo'
    )
#-----------------------CRIA A CHAVE DA CLASSE CONFORME REGRA DO ACCESS
    def codigo_categoria_classe(gr_cargo):
        return (
            'M'
            if str(gr_cargo).strip().zfill(3) in ('060', '702', '705', '706', '707')
            else 'T'
    )
    df_funcional['ChaveClass'] = df_funcional.apply(
        lambda linha:
            codigo_categoria_classe(linha['GrCargo'])
            + str(linha['GrCargo']).strip().zfill(3)
            + str(linha['Classe']).strip()
            + str(linha['REF']).strip()[:1]
            if (
                str(linha['GrCargo']).strip().zfill(3) == '705'
                and str(linha['Classe']).strip() == '4'
                and str(linha['REF']).strip()[:1] != '4'
            )
            else
            codigo_categoria_classe(linha['GrCargo'])
            + str(linha['Classe']).strip(),
        axis=1
    )
    df_funcional['DenoClasse'] = df_funcional['ChaveClass'].apply(
        lambda codigo: mapa_classe.get(codigo, '')
    )
#-----------------------CRIA A COLUNA E ESTABELECE REGRAS DE NEGOCIO DO TEM FUNCAO   
    df_funcional = df_funcional.merge( # e como o join em sql entre a funciona e pessoal
        df_pessoal[['SIAPE','Nome']], #join entre SIAPE e Nome 
        on= 'SIAPE', # achave é o SIAPE
        how='left' # e o join e´um left-join
    )    
    nome_coluna = df_funcional.pop('Nome')# remove a coluna da ultima posicao para reinserir na posição indicada

    posicao = df_funcional.columns.get_loc('SiapeDig') + 1 #aqui indica onde colocar o campo apos SiapeDig

    df_funcional.insert(# aqui inserre de fato o campo na posição
        posicao,
        'Nome',
        nome_coluna
    )
    df_funcional.insert(# faz a inserção do campo MesFita na tbl funcional
        0,#posição 1 coluna
        'MesFita', #nome da coluna
         MesFita #valor da coluna
    )
    df_funcional = df_funcional[HEADER_TIPO_2]

   # ====================================================================
   # TIPO 3 - PAGAMENTO
   # ====================================================================

    registros_tipo_3 = ler_fita_por_tipo(
        caminho_arquivo,
        LAYOUT_TIPO_3,
        '3',
        CAMPOS_DATA,
        mapas_auxiliares
    )
    print(f'Tipo_3_registro_pagamento finalizado: {len(registros_tipo_3)} registros')

    df_pagamento = pd.DataFrame(registros_tipo_3)

    df_pagamento.insert(
        0,  # primeira coluna
        'MesFita',  # nome da coluna
        MesFita  # valor
    )
  #-----------------------TRATA O CAMPO VALOR RETIRANDO OS ZEROS A ESQUERDA E DEIXANDO CO 2 CASAS DECIMAIS
    df_pagamento['Valor'] = df_pagamento['Valor'].apply(formatar_valores)

# =================================================================
# TIPO 4 - PAGAMENTO TOTAIS
# ==================================================================
    registros_tipo_4 = ler_fita_por_tipo(
        caminho_arquivo,
        LAYOUT_TIPO_4,
        '4',
        CAMPOS_DATA,
        mapas_auxiliares
    )   
    print(f'Tipo_4_registro_pagamento_totais finalizado: {len(registros_tipo_4)} registros')

    df_pagamento_totais = pd.DataFrame(registros_tipo_4)

    df_pagamento_totais['TotBruto'] = df_pagamento_totais['TotBruto'].apply(formatar_valores)
    df_pagamento_totais['TotDesc'] = df_pagamento_totais['TotDesc'].apply(formatar_valores)
    df_pagamento_totais['Liquido'] = df_pagamento_totais['Liquido'].apply(formatar_valores)
    
    df_pagamento_totais.insert( #INSERE O MES FITA NA PRIMEIRA COLUNA DE PAGAMENTOS TOTAIS
        0,  # primeira coluna
        'MesFita',  # nome da coluna
        MesFita  # valor
    )    
    df_pagamento_totais = df_pagamento_totais.merge(
        df_funcional[           
            [# USA COLUNAS DA FUNCINAL INEXISTENTES NA PAGAMENTOS TOTAIS
                'SIAPE',
                'Nome',
                'CodSituacao',
                'Situacao',
                'Categoria'
            ]
        ],
        left_on='Matric',
        right_on='SIAPE',
        how='left'
    )
    df_pagamento_totais = df_pagamento_totais[HEADER_TIPO_4]
   
# =================================================================
# TIPO 5 - AFASTAMENTO
# ==================================================================

    registros_tipo_5 = ler_fita_por_tipo(
        caminho_arquivo,
        LAYOUT_TIPO_5,
        '5',
        CAMPOS_DATA,
        mapas_auxiliares
    )   
    print(f'Tipo_5_afastamento finalizado: {len(registros_tipo_5)} registros')

    df_afastamento = pd.DataFrame(registros_tipo_5)    
    
    df_afastamento.insert( #INSERE O MES FITA NA PRIMEIRA COLUNA DE AFASTAMENTO
        0,  # primeira coluna
        'MesFita',  # nome da coluna
        MesFita  # valor
    )     
    df_afastamento = df_afastamento.merge(
        df_funcional[           
            [# USA COLUNAS DA FUNCINAL INEXISTENTES NA AFASTAMENTO
                'SIAPE',
                'Nome',
                'CodSituacao',
                'Situacao',
                'Categoria'
            ]
        ],
        left_on='SIAPE',
        right_on='SIAPE',
        how='left'
    )
    df_afastamento = df_afastamento[HEADER_TIPO_5]
 
# =================================================================
# TIPO 6 - AFASTAMENTO TOTAL
# ==================================================================

    registros_tipo_6 = ler_fita_por_tipo(
        caminho_arquivo,
        LAYOUT_TIPO_6,
        '6',
        CAMPOS_DATA,
        mapas_auxiliares
    )   

    print(f'Tipo_6_afastamento finalizado: {len(registros_tipo_6)} registros')

    df_afastamento_total = pd.DataFrame(registros_tipo_6)
    
    df_afastamento_total.insert( #INSERE O MES FITA NA PRIMEIRA COLUNA DE AFASTAMENTO
        0,  # primeira coluna
        'MesFita',  # nome da coluna
        MesFita  # valor
    )  
    
    df_afastamento_total = df_afastamento_total.merge(
        df_funcional[           
            [# USA COLUNAS DA FUNCIONAL INEXISTENTES NA AFASTAMENTO TOTAL
                'SIAPE',
                'Nome',
                'CodSituacao',
                'Situacao',               
            ]
        ],
        left_on='SIAPE',
        right_on='SIAPE',
        how='left'
    )
    df_afastamento_total = df_afastamento_total[HEADER_TIPO_6]

# ====================================================================SALVA OS DF EM CSV NO DIRETORIO E ENVIA PARA O BD MYSQL E ACCESS
       
 
# ====================================================================
    salvar_dataframe(
        df_funcional,
        'funcional.csv',
        'tbl_funcional',
        engine
    )  
    # enviar_dataframe_para_access(
    #     df_funcional,
    #     'tbl_funcional',
    #     cursor_access
    # ) 
# ====================================================================     
    salvar_dataframe(
        df_pagamento,
        'registro_pagamento.csv',
        'tbl_registro_pagamento',
        engine
    )
    # enviar_dataframe_para_access(
    #     df_pagamento,
    #     'tbl_registro_pagamento',
    #     cursor_access
    # )
# ====================================================================
    salvar_dataframe(
        df_pagamento_totais,
        'registro_pagamento_totais.csv',
        'tbl_registro_pagamento_totais',
        engine
    ) 
    # enviar_dataframe_para_access(
    #     df_pagamento_totais,
    #     'tbl_registro_pagamento_totais',
    #     cursor_access
    # ) 
# ==================================================================== 
    salvar_dataframe(
        df_afastamento,
        'afastamento.csv',
        'tbl_afastamento',
        engine
    )
    # enviar_dataframe_para_access(
    #      df_afastamento,
    #     'tbl_afastamento',
    #     cursor_access
    # ) 
# ====================================================================  
    salvar_dataframe(
        df_afastamento_total,
       'afastamento_total.csv',
       'tbl_afastamento_total',
       engine
    )
    # enviar_dataframe_para_access(
    #     df_afastamento_total,
    #    'tbl_afastamento_total',
    #     cursor_access
    # ) 
    # conexao_access.commit()

    # cursor_access.close()
    # conexao_access.close()

    # print('✅ Tabelas principais enviadas para o Access!')
  
   # ====================================================================
    # CRIAÇÃO DE TABELA tbl_pgto_incentivo_qualificacao
   # ====================================================================

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

    # ====================================================================
    # MAPA PERQUALIF
    # ====================================================================

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

    # ====================================================================
    # ESCOLARIDADE FINAL
    # ====================================================================

    df_pessoal = criar_escolaridade(
        df_pessoal,
        df_titulacao_correcao,
        mapa_perqualif
    )
    df_pessoal = df_pessoal[HEADER_TIPO_1]

    salvar_dataframe(
        df_pessoal,
        'pessoal.csv',
        'tbl_pessoal',
        engine
    ) 
    # enviar_dataframe_para_access(
    #     df_pessoal,
    #     'tbl_pessoal',
    #     cursor_access
    # ) 
else:
    print("❌ ERRO: Arquivo fita não encontrado.")
    print("📁 Caminho esperado:")
    print(caminho_arquivo)
    print("Verifique se o arquivo foi copiado para a pasta auto_fita_espelho.")