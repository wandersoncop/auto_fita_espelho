import pyodbc


caminho_banco_access = r"C:\Users\Wanderson\Documents\auto_fita.accdb"


def conectar_access():
    conexao = pyodbc.connect(
        rf"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};"
        rf"DBQ={caminho_banco_access};"
    )
    print("✅ Conectado ao Access com sucesso!")
    return conexao
    
def executar_sql(sql):
    conexao = conectar_access()
    cursor = conexao.cursor()

    cursor.execute(sql)

    conexao.commit()

    cursor.close()
    conexao.close()

def consultar_sql(sql):
    conexao = conectar_access()
    cursor = conexao.cursor()

    cursor.execute(sql)

    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultados


