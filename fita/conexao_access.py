import pyodbc


caminho_banco_access = r"C:\Users\Wanderson\Documents\auto_fita.accdb"


def conectar_access():
    conexao = pyodbc.connect(
        rf"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};"
        rf"DBQ={caminho_banco_access};"
    )

    print("✅ Conectado ao Access com sucesso!")
    return conexao


if __name__ == "__main__":
    conexao = conectar_access()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE teste_conexao (
            id INTEGER,
            nome TEXT(100)
        )
    """)

    cursor.execute("""
        INSERT INTO teste_conexao (id, nome)
        VALUES (1, 'Teste Access')
    """)

    conexao.commit()

    print("✅ Tabela teste_conexao criada com sucesso!")

    cursor.execute("SELECT * FROM teste_conexao")

    for linha in cursor.fetchall():
        print(linha)

    conexao.close()