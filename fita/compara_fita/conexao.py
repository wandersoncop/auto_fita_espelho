"""cria a conexao com o banco Mysql"""

from sqlalchemy import create_engine, text
from terminal import ok, info, aviso, erro

HOST = "localhost"
USUARIO = "root"
SENHA = "123456"
BANCO = "auto_fita_espelho"


def criar_banco():
    """
    Cria o banco caso ele não exista.
    """

    engine_temp = create_engine(
        f"mysql+pymysql://{USUARIO}:{SENHA}@{HOST}"
    )

    with engine_temp.connect() as conexao:
        conexao.execute(
            text(
                f"""
                CREATE DATABASE IF NOT EXISTS {BANCO}
                CHARACTER SET utf8mb4
                COLLATE utf8mb4_unicode_ci
                """
            )
        )
        conexao.commit()

        print()
        aviso(f"Banco {BANCO} verificado / criado com sucesso!")
        print()


# cria o banco antes de conectar
criar_banco()

# conecta no banco
engine = create_engine(
    f"mysql+pymysql://{USUARIO}:{SENHA}@{HOST}/{BANCO}"
)

try:
    with engine.connect() as conexao:
       aviso("Banco de dados conectado com sucesso!")

except Exception as e:
    erro(f"Falha na conexão com o banco: {e}")