import os
import pandas as pd
from conexao_access import conectar_access
from envia_access import enviar_dataframe_para_access


diretorio = os.path.join(
    os.path.expanduser("~"),
    "Desktop",
    "auto_fita_espelho",
    "tbl_Auxiliares"
)


