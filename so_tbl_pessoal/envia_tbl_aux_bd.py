import os
import pandas as pd
from conexao import engine


#---------------------------CAMINHO PARA A PASTA DE TABELAS AUXILIARES
diretorio = os.path.join(
    os.path.expanduser('~'),
    'desktop',
    'auto_fita_espelho',
    'tbl_Auxiliares'
)
#---------------------------TABELAS AUXILIARES
"""
    Todas as tabelas devem estar:
    em .txt
    com a primeira linha de cabeçalho
    padrão Unicode(UTF-8)  
    separados por ';' 
    e entre ""
    o sitema enviará tudo como texto para o bd
"""
#-----------------------ESTADO CIVIL

tbl_estado_civil = os.path.join(diretorio, 'Tabela Estado Civil.txt')
df_estado_civil= pd.read_csv(tbl_estado_civil, sep=';',encoding='latin-1',dtype=str)
df_estado_civil.to_sql( 'aux_estado_civil',engine,if_exists='replace',index=False)
print ('Tabela estado civil enviada')

#-----------------------pais

tbl_pais = os.path.join(diretorio, 'Tabela Pais.txt')
df_pais= pd.read_csv(tbl_pais, sep=';',encoding='latin-1',dtype=str)
df_pais.to_sql( 'aux_pais',engine,if_exists='replace',index=False)
print ('Tabela Pais enviada')

#-----------------------escolaridade

tbl_escolaridade = os.path.join(diretorio,'Tabela Escolaridade.txt')
df_escolaridade = pd.read_csv(tbl_escolaridade,sep=';',encoding='latin-1',dtype=str)
df_escolaridade.to_sql('aux_escolaridade',engine,if_exists='replace',index=False)
print('Tabela Escolaridade enviada')

#-----------------------titulação

tbl_titulacao = os.path.join(diretorio,'Tabela Titulacao.txt')
df_titulacao = pd.read_csv(tbl_titulacao,sep=';',encoding='latin-1',dtype=str)
df_titulacao.to_sql('aux_titulacao',engine,if_exists='replace',index=False)
print('Tabela Titulacao enviada')

#-----------------------titulação correção

tbl_titulacao_correcao = os.path.join(diretorio,'Tabela Titulacao Correção.txt')
df_titulacao_correcao = pd.read_csv(tbl_titulacao_correcao,sep=';',encoding='latin-1',dtype=str)
df_titulacao_correcao.to_sql('aux_titulacao_correcao',engine,if_exists='replace',index=False)
print('Tabela Titulação Correção enviada')

#-----------------------rubrica icq

tbl_rubrica_incentivo_qualificacao = os.path.join(diretorio,'Tabela Rubrica Incentivo Qualificacao.txt')
df_rubrica_incentivo_qualificacao = pd.read_csv(tbl_rubrica_incentivo_qualificacao,sep=';',encoding='latin-1',dtype=str)
df_rubrica_incentivo_qualificacao.to_sql('aux_rubrica_incentivo_qualificacao',engine,if_exists='replace',index=False)
print('Tabela Rubrica Incentivo Qualificacao enviada')

#-----------------------pescad

tbl_pescad_Insc_Ufmg = os.path.join(diretorio,'Pescad_InscUFMG.txt')
df_pescad_Insc_Ufmg = pd.read_csv(tbl_pescad_Insc_Ufmg,sep=';',encoding='latin-1',dtype=str)
df_pescad_Insc_Ufmg.to_sql('aux_pescad_insc_ufmg',engine,if_exists='replace',index=False)
print('Tabela Pescad Isnc UFMG enviada')


#-----------------------situação

tbl_situacao = os.path.join(diretorio, 'Tabela Situacao.txt')
df_situacao= pd.read_csv(tbl_situacao, sep=';',encoding='latin-1',dtype=str)
df_situacao.to_sql( 'aux_situacao',engine,if_exists='replace',index=False)
print ('Tabela Situacao enviada')
