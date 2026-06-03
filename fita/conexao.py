"""cria a conexao com o banco Mysql"""
from sqlalchemy import create_engine
engine = create_engine(
    "mysql+pymysql://root:123456@localhost/auto_fita_espelho"
    # "mysql+pymysql://root:123456@localhost/fita_pessoal"
)
try:
    with engine.connect() as conexao:
        print("Conectado com sucesso!")

except Exception as erro:
    print(f"Erro: {erro}")