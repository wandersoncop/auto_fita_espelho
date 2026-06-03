import pandas as pd
from conexao import engine

df_export = pd.read_sql(
       """
    SELECT
       *
    FROM auto_fita_espelho.tbl_funcional;
    """,
    engine
)

df_export.to_csv(
    "tbl_funcional_exportada.txt",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("✅ Arquivo exportado com sucesso!")