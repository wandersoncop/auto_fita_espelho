def enviar_dataframe_para_access(dataframe, nome_tabela, cursor):
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

    dados = dataframe.fillna("").astype(str).values.tolist()

    cursor.executemany(sql_insert, dados)

    print(f"✅ Tabela {nome_tabela} enviada para o Access")