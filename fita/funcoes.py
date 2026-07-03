import pandas as pd
import os
import shutil
import sys
from sqlalchemy import text

def extrair_tipos(linha, layout, campos_data=None, mapas_auxiliares=None):
    """Traduz uma linha da fita espelho usando as posições do layout."""

    if campos_data is None:
        campos_data = []

    if mapas_auxiliares is None:
        mapas_auxiliares = {}

    registro = {} #cria um dicionario vazio quando percorre o layout coloca o valor da linha EX na fita:
                  #"CodEstadoCiv":(161,162) 
                  #valor = linha[161:162].strip()
                  #valor = '1'

    for nome_campo, posicoes in layout.items():
        inicio, fim = posicoes

        valor = linha[inicio:fim].strip()

        if nome_campo in campos_data:
            valor = formatar_data(valor)

        if nome_campo == 'Sexo':
            valor = formatar_sexo(valor)

        registro[nome_campo] = valor #aqui pega o valor la do começo
                                     #vira = registro['CodEstadoCiv'] = '1'

        if nome_campo in mapas_auxiliares:
            nome_campo_novo = mapas_auxiliares[nome_campo]['nome_campo']
            mapa = mapas_auxiliares[nome_campo]['mapa']
           
            #FAZ A VERIFICAÇÃO DE CAMPO SEM TRADUÇÃO

            if valor not in mapa:
                if nome_campo == 'SIAPE':
                    registro [nome_campo_novo] = ''
                else:
                    raise ValueError(
                        f'❌ Tradução não encontrada para {nome_campo}: "{valor}"'
                )
            else:    
                registro[nome_campo_novo] = mapa[valor]
            
          #PARA VERIFICAR OS CAMPOS QUE FALTAM TRADUÇÃO COMENTAR APOS USO E NÃO APAGAR  
            # if valor not in mapa:
            #     print(f'❌ Tradução não encontrada para {nome_campo}: "{valor}"')
            #     registro[nome_campo_novo] = ''
            # else:
            #         registro[nome_campo_novo] = mapa[valor]
           #============================================================================ 

    return registro

def extrair_tipo_0(caminho_arquivo):
    """Extrai o mês da fita."""

    with open(caminho_arquivo, encoding='latin-1') as arquivo_txt:

        for linha in arquivo_txt:

            if len(linha) > 18 and linha[17] == '0':
                mes = linha[45:47]
                ano = linha[47:51]

                return f"{ano}_{mes}"
    return "0000_00"

def ler_fita_por_tipo(caminho_arquivo,layout,tipo_registro,campos_data=None,mapas_auxiliares=None):
    """Lê os registros da fita e os separa por tipo."""

    registros = []

    with open(caminho_arquivo, encoding='latin-1') as arquivo_txt:
        for linha in arquivo_txt:
            if len(linha) > 18 and linha[17] == tipo_registro:
                dados = extrair_tipos(
                    linha,
                    layout,
                    campos_data,
                    mapas_auxiliares
                )

                if 'GrCargo' in dados and mapas_auxiliares is not None:

                    #---------------------------------------- CRIAÇÃO Categoria ---

                    gr_cargo = dados.get('GrCargo', '')

                    cat_letra = (
                        'M'
                        if gr_cargo in ('060','702','705','706','707')
                        else 'T'
                    )

                    dados['Categoria'] = (
                        'Docente'
                        if cat_letra == 'M'
                        else 'Tec-Administrativo'
                    )

                    #---------------------------------------- CRIAÇÃO RegimeTrab ---

                    valor_rtrab = dados.get('RTRAB','').strip()
                    dados['RegimeTrab'] = 'DE' if valor_rtrab == '99' else valor_rtrab

                    #---------------------------------------- CRIAÇÃO CodCargo ---

                    valor_grcargo = dados.get('GrCargo','').strip()
                    valor_cargo = dados.get('Cargo','').strip()
                    dados['CodCargo'] = valor_grcargo + valor_cargo

                    #---------------------------------------- CRIAÇÃO deno classe ---

                    valor_classe = dados.get('Classe', '').strip()
                    ref = dados.get('REF', '').strip()
                    primeiro_dig_ref = ref[0] if ref else ""

                    chave_final = f"{cat_letra}{valor_classe}"

                    if valor_grcargo == '705' and valor_classe == '4' and primeiro_dig_ref != '4':
                        chave_final = f"{cat_letra}{valor_grcargo}{valor_classe}{primeiro_dig_ref}"

                    dados['ChaveClass'] = chave_final

                    dados['DenoClasse'] = (
                        mapas_auxiliares['ChaveClass']['mapa'].get(
                            chave_final,
                            ''
                        )
                    )

                registros.append(dados)

    return registros

def formatar_data(valor):
    """Formata os campos de data da fita espelho."""

    if valor == '00000000':
        return ''

    if valor and len(valor) == 8 and valor.isdigit():
        return f'{valor[0:2]}/{valor[2:4]}/{valor[4:8]}'

    return valor

def formatar_sexo(valor):
    """ trasforma os valores de M F para Masculino e Feminino"""
    if valor == 'M':
        return 'Masculino'
    if valor =='F':
        return'Feminino'
    return valor

def criar_escolaridade(df_pessoal, df_titulacao_correcao, mapa_perqualif=None):
    """Cria o campo Escolaridade comparando escolaridade e titulação."""

    if mapa_perqualif is None:
        mapa_perqualif = {}

    mapa_escolaridade = (
        df_titulacao_correcao
        .dropna(subset=['codEscolaridade'])
        .set_index('codEscolaridade')
        .to_dict('index')
    )

    mapa_titulacao = (
        df_titulacao_correcao
        .dropna(subset=['codTitulacao'])
        .set_index('codTitulacao')
        .to_dict('index')
    )

    escolaridades = []

    for _, linha in df_pessoal.iterrows():

        cod_escolaridade = linha['CodEscolaridade']
        cod_titulacao = linha['CodTitulacao']
        deno_escolaridade = linha['DenoEscolaridade']
        siape = linha['SIAPE']
        perqualif = str(mapa_perqualif.get(siape, '')).strip()

        dados_escolaridade = mapa_escolaridade.get(cod_escolaridade)
        dados_titulacao = mapa_titulacao.get(cod_titulacao)

        if cod_titulacao in ('', '00'):

            if perqualif in ('52', '50', '35'):
                escolaridades.append('MESTRADO')
                continue

            if perqualif == '75':
                escolaridades.append('DOUTORADO')
                continue

            if perqualif == '30':
                escolaridades.append('ESPECIALIZACAO NIVEL SUPERIOR')
                continue

        if dados_escolaridade and dados_titulacao:

            grau_escolaridade = int(
                dados_escolaridade['grauEscolaridade']
            )

            grau_titulacao_valor = dados_titulacao['grauEscolaridade']

            if pd.isna(grau_titulacao_valor):
                grau_titulacao = None
            else:
                grau_titulacao = int(grau_titulacao_valor)

            if grau_titulacao is not None:

                if grau_escolaridade > grau_titulacao:
                    escolaridades.append(
                        dados_escolaridade['denoEscolaridade']
                    )
                else:
                    escolaridades.append(
                        dados_titulacao['denoEscolaridade']
                    )

            else:
                escolaridades.append(
                    dados_escolaridade['denoEscolaridade']
                )

        else:
            escolaridades.append(
                deno_escolaridade
            )

    if 'Escolaridade' in df_pessoal.columns:
        df_pessoal = df_pessoal.drop(columns=['Escolaridade'])

    posicao = df_pessoal.columns.get_loc('CodTitulacao')

    df_pessoal.insert(
        posicao,
        'Escolaridade',
        escolaridades
    )

    return df_pessoal     

def formatar_valores(valor):
    """
        converte a sequencia de numeros em valores
        monetarios sem os zeros as esquerda e com duas
        casas decimais
    """
    return round(
        pd.to_numeric(valor,errors='coerce')/100,2
    )

def salvar_dataframe(df,nome_csv,nome_tabela,engine,MesFita):
    """
        salva o dataframe em csv e envia para o banco de dados.
    """   

    pasta_saida = os.path.join(
       obter_pasta_base(),
        'Saida',
        MesFita
    ) 
    os.makedirs(pasta_saida,exist_ok=True)    
    caminho_csv = os.path.join(
        pasta_saida,
        nome_csv
    )
    df.to_csv(caminho_csv,sep=';',decimal=',',index=False,encoding='utf-8-sig'
    )
    # print(f"✅ CSV {nome_csv} exportado com sucesso!")
    # print(caminho_csv)

    with engine.begin() as conexao:
        conexao.execute(
            text(f'DELETE FROM {nome_tabela} WHERE MesFita = :MesFita'),
            {'MesFita':MesFita}
        )

    df.to_sql(
        nome_tabela,
        engine,
        if_exists='append',
        index=False
    )
    print(f"✅ {nome_csv:<32} -> {nome_tabela}")
    # print(f"✅ {nome_tabela} salvo no banco!")

def obter_pasta_base():
    """
    Retorna a pasta base do sistema.

    Quando roda pelo Python:
    C:/Users/wandersoncop/Desktop/auto_fita_espelho

    Quando roda pelo EXE:
    pasta onde está o AutoFita.exe.
    """

    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)

    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def arquivar_fita_processada(caminho_arquivo, MesFita):
    """
        Move a fita processsada para a pasta Processadas
    """
    ano = MesFita[:4]

    pasta_processadas = os.path.join(
        obter_pasta_base(),
        'Entrada',
        'Processadas',
        ano
    )
    os.makedirs(pasta_processadas,exist_ok=True)

    nome_arquivo = os.path.basename(caminho_arquivo)

    destino = os.path.join(
        pasta_processadas,
        nome_arquivo
    )

    shutil.move(caminho_arquivo,destino)

    print(f"📦 {nome_arquivo} arquivada.")
