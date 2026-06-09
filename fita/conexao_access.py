import os
import pyodbc



# caminho_banco_access = r"C:\Users\Wandersoncop\Documents\auto_fita.accdb"

caminho_banco_access = os.path.join(
    os.path.expanduser('~'),
    'Documents',
    'auto_fita.accdb'
)


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

if __name__ == "__main__":
    print(caminho_banco_access)

    conexao = conectar_access()

    print(conexao)

    conexao.close()
