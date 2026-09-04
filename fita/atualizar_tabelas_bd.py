import os
import pandas as pd
from conexao import engine
from funcoes import obter_pasta_base
from sqlalchemy import inspect
def main():
    """
        Todas as tabelas devem estar:
        em .txt
        com a primeira linha de cabeçalho
        padrão Unicode(UTF-8)
        separados por ';'
        e entre ""
        o sitema enviará tudo como texto para o bd
    """
    #---------------------------CAMINHO PARA A PASTA DE TABELAS AUXILIARES
    diretorio = os.path.join(
        obter_pasta_base(),
        'tbl_Auxiliares'
    )
    #---------------------------TABELAS AUXILIARES

    # -----------------------ESTADO CIVIL

    tbl_estado_civil = os.path.join(diretorio, 'Tabela Estado Civil.txt')
    df_estado_civil= pd.read_csv(tbl_estado_civil, sep=';',encoding='latin-1',dtype=str)
    df_estado_civil.to_sql( 'aux_estado_civil',engine,if_exists='replace',index=False)

    # -----------------------PAIS

    tbl_pais = os.path.join(diretorio, 'Tabela Pais.txt')
    df_pais= pd.read_csv(tbl_pais, sep=';',encoding='latin-1',dtype=str)
    df_pais.to_sql( 'aux_pais',engine,if_exists='replace',index=False)
    # print ('Tabela Pais enviada')

    #-----------------------CARGO

    tbl_cargo = os.path.join(diretorio, 'Tabela Cargo.txt')
    df_cargo= pd.read_csv(tbl_cargo, sep=';',encoding='latin-1',dtype=str)
    df_cargo.to_sql( 'aux_cargo',engine,if_exists='replace',index=False)
    # print ('Tabela Cargo enviada')

    #-----------------------SITUAÇÃO

    tbl_situacao = os.path.join(diretorio, 'Tabela Situacao.txt')
    df_situacao= pd.read_csv(tbl_situacao, sep=';',encoding='latin-1',dtype=str)
    df_situacao.to_sql( 'aux_situacao',engine,if_exists='replace',index=False)
    # print ('Tabela Situacao enviada')

    #-----------------------ATIVIDADE

    tbl_atividade = os.path.join(diretorio, 'Tabela Atividade.txt')
    df_atividade= pd.read_csv(tbl_atividade, sep=';',encoding='latin-1',dtype=str)
    df_atividade.to_sql( 'aux_atividade',engine,if_exists='replace',index=False)
    # print ('Tabela Atividade enviada')

    #-----------------------CLASSE

    tbl_classe = os.path.join(diretorio,'Tabela Classe.txt')
    df_classe = pd.read_csv(tbl_classe, sep=';',encoding='utf-8-sig',dtype=str)
    df_classe.to_sql( 'aux_classe',engine,if_exists='replace',index=False)
    # print('Tabela Classe enviada')

    #-----------------------ESCOLARIDADE

    tbl_escolaridade = os.path.join(diretorio,'Tabela Escolaridade.txt')
    df_escolaridade = pd.read_csv(tbl_escolaridade,sep=';',encoding='latin-1',dtype=str)
    df_escolaridade.to_sql('aux_escolaridade',engine,if_exists='replace',index=False)
    # print('Tabela Escolaridade enviada')

    # #-----------------------TITULAÇÃO

    tbl_titulacao = os.path.join(diretorio,'Tabela Titulacao.txt')
    df_titulacao = pd.read_csv(tbl_titulacao,sep=';',encoding='utf-8-sig',dtype=str)
    df_titulacao.to_sql('aux_titulacao',engine,if_exists='replace',index=False)
    # print('Tabela Titulacao enviada')

    #-----------------------LOCAL APOSENTADORIA

    inspetor = inspect(engine)
    if not inspetor.has_table('aux_local_aposentadoria'):
        print('Primeira carga da aux_local_aposentadoria...')

        tbl_local_aposentadoria = os.path.join(
            diretorio,
            'Tabela Local Aposentadoria.txt'
        )
        df_local_aposentadoria = pd.read_csv(
            tbl_local_aposentadoria,
            sep=';',
            encoding='utf-8-sig',
            dtype=str)
        df_local_aposentadoria.to_sql(
            'aux_local_aposentadoria',
            engine,
            if_exists='replace',
            index=False)
    # print('Tabela Local Aposentadoria enviada')

    #-----------------------MUNICIPIO

    tbl_municipio = os.path.join(diretorio,'Tabela Municipio.txt')
    df_municipio = pd.read_csv(tbl_municipio,sep=';',encoding='latin-1',dtype=str)
    df_municipio.to_sql('aux_municipio',engine,if_exists='replace',index=False)
    # print('Tabela Municipio enviada')


    #-----------------------UORG ENDEREÇO

    tbl_uorg_endereco = os.path.join(diretorio,'Tabela UORG Endereco.txt')
    df_uorg_endereco = pd.read_csv(tbl_uorg_endereco,sep=';',encoding='latin-1',dtype=str)
    df_uorg_endereco.to_sql('aux_uorg_endereco',engine,if_exists='replace',index=False)
    # print('Tabela UORG Endereco enviada')

    #-----------------------TITULAÇÃO CORREÇÃO

    tbl_titulacao_correcao = os.path.join(diretorio,'Tabela Titulacao Correção.txt')
    df_titulacao_correcao = pd.read_csv(tbl_titulacao_correcao,sep=';',encoding='latin-1',dtype=str)
    df_titulacao_correcao.to_sql('aux_titulacao_correcao',engine,if_exists='replace',index=False)
    # print('Tabela Titulação Correção enviada')

    #-----------------------RUBRICA ICQ

    tbl_rubrica_incentivo_qualificacao = os.path.join(diretorio,'Tabela Rubrica Incentivo Qualificacao.txt')
    df_rubrica_incentivo_qualificacao = pd.read_csv(tbl_rubrica_incentivo_qualificacao,sep=';',encoding='latin-1',dtype=str)
    df_rubrica_incentivo_qualificacao.to_sql('aux_rubrica_incentivo_qualificacao',engine,if_exists='replace',index=False)
    # print('Tabela Rubrica Incentivo Qualificacao enviada')

    #-----------------------RUBRICA

    tbl_rubrica = os.path.join(diretorio,'Tabela Rubrica.txt')
    df_rubrica = pd.read_csv(tbl_rubrica,sep=';',encoding='latin-1',dtype=str)
    df_rubrica.to_sql('aux_rubrica',engine,if_exists='replace',index=False)
    # print('Tabela Rubrica enviada')

    #-----------------------OCORRENCIA

    tbl_ocorrencia = os.path.join(diretorio,'Tabela Ocorrencia.txt')
    df_ocorrencia = pd.read_csv(tbl_ocorrencia,sep=';',encoding='latin-1',dtype=str)
    df_ocorrencia.to_sql('aux_ocorrencia',engine,if_exists='replace',index=False)
    # print('Tabela Ocorrencia enviada')

    #-----------------------ORGÃOS

    tbl_orgaos = os.path.join(diretorio,'Tabela Orgaos.txt')
    df_orgaos = pd.read_csv(tbl_orgaos,sep=';',encoding='latin-1',dtype=str)
    df_orgaos.to_sql('aux_orgaos',engine,if_exists='replace',index=False)
    # print('Tabela Orgaos enviada')

    #-----------------------PESCAD

    tbl_pescad = os.path.join(diretorio,'Pescad_InscUFMG.txt')
    df_pescad = pd.read_csv(tbl_pescad,sep=';',encoding='latin-1',dtype=str)
    df_pescad.to_sql('aux_pescad_insc_ufmg',engine,if_exists='replace',index=False)
    # print('Tabela Pescad enviada')

    #-----------------------cad_apf resolve situação da categoria MAGISTERIO X TEC-ADMINISTRATIVO

    tbl_cad_apf = os.path.join(diretorio,'CadAPF.txt')
    tbl_cad_apf = pd.read_csv(tbl_cad_apf,sep=';',encoding='utf-8-sig',dtype=str)
    tbl_cad_apf.to_sql('aux_cad_apf',engine,if_exists='replace',index=False)
    # print('Tabela CadAPF enviada')

    #-----------------------CRIA UNIDADE ATUAL SERÁ ENVIADA UMA UNICA VEZ (BASE INCREMENTAL)

    inspetor = inspect(engine)

    if not inspetor.has_table('aux_unidade_atual'):
        print('Primeira carga da aux_unidade_atual...')

        tbl_unidade_atual = os.path.join(diretorio,'Tabela Unidade Atual.txt')
        df_unidade_atual = pd.read_csv(tbl_unidade_atual,sep=';',encoding='utf-8-sig',dtype=str)

        df_unidade_atual.to_sql('aux_unidade_atual',engine,if_exists='replace',index=False)


    #-----------------------CRIA UNIDADE ATUAL

    tbl_uorgs = os.path.join(diretorio, 'Extr_UORGs.txt')
    df_uorgs = pd.read_csv(tbl_uorgs, sep=';', encoding='latin1', dtype=str)

    tbl_uorgs = os.path.join(diretorio, 'Extr_UORGs.txt')
    df_uorgs = pd.read_csv(
        tbl_uorgs,
        sep=';',
        encoding='latin1',
        dtype=str
    )

    #  aqui sera criada a tabela unidade atual, que não pode ser apagada a primeira inserção tem que ser a que esta na fita!!!!!
    # para poder trazer as inserçoes antigas pois a tabela é incremental
    # CodUnid: "000" & Direita([NrUorg];6)
    df_uorgs['NrUorg'] = (
        '000'
        + df_uorgs['NrUorg'].str[-6:]
    )

    df_uorgs = df_uorgs.rename(
        columns={
            'NrUorg': 'CodUnid'
        }
    )

    tbl_nome_uorg_pai = os.path.join(diretorio, 'Tabela Nome Uorg Pai.txt')
    df_nome_uorg_pai = pd.read_csv(tbl_nome_uorg_pai, sep=';', encoding='latin1', dtype=str)

    # NomeUorgPai: tradução de UorgPai
    mapa_nome_uorg_pai = dict(
        zip(
            df_nome_uorg_pai['UorgPai'],
            df_nome_uorg_pai['NomeUorg']
        )
    )

    df_uorgs['NomeUorgPai'] = df_uorgs['UorgPai'].map(mapa_nome_uorg_pai)
    df_uorgs['NomeUorgPai'] = df_uorgs['NomeUorgPai'].fillna('')

    # Unid: 3 primeiras letras do NomeUorg
    df_uorgs['Unid'] = df_uorgs['NomeUorg'].fillna('').str[:3]

    # DenoSetor
    df_uorgs['DenoSetor'] = df_uorgs.apply(
        lambda linha:
            str(linha['NomeUorg'])
            if '-' in str(linha['NomeUorg'])
            else str(linha['Unid']) + '-' + str(linha['NomeUorg']),
        axis=1
    )

    # Data de cadastro
    df_uorgs['DtCadUorgFita'] = pd.Timestamp.now()

    # Mantém somente as colunas finais, na ordem da tabela antiga
    df_uorgs = df_uorgs[
        [
            'CodUnid',
            'SiglaUorg',
            'Unid',
            'DenoSetor',
            'DtCriacaoUorg',
            'DtExtincaoUorg',
            'UorgPai',
            'NomeUorgPai',
            'DtCadUorgFita'
        ]
    ]

    caminho_csv_saida= os.path.join(diretorio,'aux_unidade_atual.csv')

    # print(f'tabela unidade atual {caminho_csv_saida}')

    df_existente = pd.read_sql(
        "SELECT CodUnid FROM aux_unidade_atual",
        engine
    )

    cod_existentes = set(# set ira trazer somente o que não for repetido
        df_existente['CodUnid'].astype(str) # vai tranformar o CodUnid em texto
    )
    df_novos = df_uorgs[
        ~df_uorgs['CodUnid'].astype(str).isin(cod_existentes) # vai trazer o CodUnid que não estiver em cod_existente
    ]


    if len(df_novos) > 0:
        df_novos.to_sql(
            'aux_unidade_atual',
            engine,
            if_exists='append',
            index=False
        )
        print(f"✔ Unidade Atual: {len(df_novos)} novo(s) registro(s) adicionados.")


    df_final = pd.read_sql(
        "SELECT * FROM aux_unidade_atual",
        engine
    )

    caminho_csv_saida = os.path.join(
        diretorio,
        'aux_unidade_atual.csv'
    )

    df_final.to_csv(
        caminho_csv_saida,
        sep=';',
        index=False,
        encoding='utf-8-sig'
    )


if __name__ == "__main__":
    main()
