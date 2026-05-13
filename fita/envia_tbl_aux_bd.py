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

df_estado_civil.to_sql( 'aux_estado_civil',engine,if_exists='replace',index=False)
print ('Tabela estado civil enviada')

#-----------------------PAIS

tbl_pais = os.path.join(diretorio, 'Tabela Pais.txt')

df_Pais= pd.read_csv(tbl_pais, sep=';',encoding='latin-1',dtype=str)

df_Pais.to_sql( 'aux_pais',engine,if_exists='replace',index=False)
print ('Tabela Pais enviada')

#-----------------------cargo

tbl_Cargo = os.path.join(diretorio, 'Tabela Cargo.txt')

df_Cargo= pd.read_csv(tbl_Cargo, sep=';',encoding='latin-1',dtype=str)

df_Cargo.to_sql( 'aux_Cargo',engine,if_exists='replace',index=False)
print ('Tabela Cargo enviada')

#-----------------------situação

tbl_situacao = os.path.join(diretorio, 'Tabela Situacao.txt')

df_Situacao= pd.read_csv(tbl_situacao, sep=';',encoding='latin-1',dtype=str)

df_Situacao.to_sql( 'aux_situacao',engine,if_exists='replace',index=False)
print ('Tabela Situacao enviada')
