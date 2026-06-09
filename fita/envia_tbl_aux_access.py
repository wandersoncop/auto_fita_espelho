import os
import pandas as pd
from conexao_access import conectar_access


diretorio = os.path.join(
    os.path.expanduser("~"),
    "Desktop",
    "auto_fita_espelho",
    "tbl_Auxiliares"
)


def enviar_dataframe_para_access(dataframe, nome_tabela,cursor):
    
    try:
        cursor.execute(f"DROP TABLE [{nome_tabela}]")
    except:
        pass

    colunas = dataframe.columns.tolist()

    campos_sql = ", ".join([
        f"[{coluna}] TEXT(255)"
        for coluna in colunas
    ])

    cursor.execute(f"""
        CREATE TABLE [{nome_tabela}] (
            {campos_sql}
        )
    """)

    nomes_colunas = ", ".join([
        f"[{coluna}]"
        for coluna in colunas
    ])

    parametros = ", ".join(["?" for _ in colunas])

    sql_insert = f"""
        INSERT INTO [{nome_tabela}]
        ({nomes_colunas})
        VALUES ({parametros})
    """

    dados = dataframe.fillna("").values.tolist()

    cursor.executemany(sql_insert, dados)

    

    print(f"✅ Tabela {nome_tabela} enviada para o Access")


def carregar_e_enviar(nome_arquivo, nome_tabela, encoding,cursor):
    caminho_arquivo = os.path.join(diretorio, nome_arquivo)

    dataframe = pd.read_csv(
        caminho_arquivo,
        sep=";",
        encoding=encoding,
        dtype=str
    )

    enviar_dataframe_para_access(dataframe, nome_tabela,cursor)


tabelas = [
    ("Tabela Estado Civil.txt", "aux_estado_civil", "latin-1"),
    ("Tabela Pais.txt", "aux_pais", "latin-1"),
    ("Tabela Cargo.txt", "aux_cargo", "latin-1"),
    ("Tabela Situacao.txt", "aux_situacao", "latin-1"),
    ("Tabela Atividade.txt", "aux_atividade", "latin-1"),
    ("Tabela Classe.txt", "aux_classe", "latin-1"),
    ("Tabela Escolaridade.txt", "aux_escolaridade", "latin-1"),
    ("Tabela Titulacao.txt", "aux_titulacao", "latin-1"),
    ("Tabela Local Aposentadoria.txt", "aux_local_aposentadoria", "latin-1"),
    ("Tabela Municipio.txt", "aux_municipio", "latin-1"),
    ("Tabela Unidade Atual.txt", "aux_unidade_atual", "latin-1"),
    ("Tabela UORG Endereco.txt", "aux_uorg_endereco", "latin-1"),
    ("Tabela Titulacao Correção.txt", "aux_titulacao_correcao", "latin-1"),
    ("Tabela Rubrica Incentivo Qualificacao.txt", "aux_rubrica_incentivo_qualificacao", "latin-1"),
    ("Tabela Ocorrencia.txt", "aux_ocorrencia", "latin-1"),
    ("Tabela Orgaos.txt", "aux_orgaos", "latin-1"),
    ("Pescad_InscUFMG.txt", "aux_pescad_insc_ufmg", "latin-1"),
    ("CadAPF.txt", "aux_cad_apf", "utf-8-sig"),
    ("Tabela Rubrica.txt", "aux_rubrica", "utf-8-sig"),
]


conexao = conectar_access()

cursor = conexao.cursor()

for nome_arquivo, nome_tabela, encoding in tabelas:

    carregar_e_enviar(
        nome_arquivo,
        nome_tabela,
        encoding,
        cursor
    )

conexao.commit()

cursor.close()
conexao.close()

print(
    "✅ Todas as tabelas auxiliares foram enviadas para o Access!"
)
  