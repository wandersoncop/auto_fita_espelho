import os
import pandas as pd
from conexao import engine

diretorio = os.path.join(
    os.path.expanduser('~'),
    'desktop',
    'auto_fita_espelho'
)
#-----------------------ESTADO CIVIL

tbl_estado_civil = os.path.join(diretorio, 'Tabela Estado Civil.txt')

df_estado_civil= pd.read_csv(tbl_estado_civil, sep=';',encoding='latin-1',dtype=str)

df_estado_civil.to_sql( 'estado_civil',engine,if_exists='replace',index=False)
print ('Tabela estado civil enviada')

#-----------------------PAIS

tbl_pais = os.path.join(diretorio, 'Tabela Pais.txt')

df_Pais= pd.read_csv(tbl_pais, sep=';',encoding='latin-1',dtype=str)

df_Pais.to_sql( 'pais',engine,if_exists='replace',index=False)
print ('Tabela Pais enviada')