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
#----------------------------------------------TABELAS AUXILIARES----------------------------------------------
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

#-----------------------PAIS

tbl_pais = os.path.join(diretorio, 'Tabela Pais.txt')
df_pais= pd.read_csv(tbl_pais, sep=';',encoding='latin-1',dtype=str)
df_pais.to_sql( 'aux_pais',engine,if_exists='replace',index=False)
print ('Tabela Pais enviada')

#-----------------------cargo

tbl_cargo = os.path.join(diretorio, 'Tabela Cargo.txt')
df_cargo= pd.read_csv(tbl_cargo, sep=';',encoding='latin-1',dtype=str)
df_cargo.to_sql( 'aux_cargo',engine,if_exists='replace',index=False)
print ('Tabela Cargo enviada')

#-----------------------situação

tbl_situacao = os.path.join(diretorio, 'Tabela Situacao.txt')
df_situacao= pd.read_csv(tbl_situacao, sep=';',encoding='latin-1',dtype=str)
df_situacao.to_sql( 'aux_situacao',engine,if_exists='replace',index=False)
print ('Tabela Situacao enviada')

#-----------------------atividade

tbl_atividade = os.path.join(diretorio, 'Tabela Atividade.txt')
df_atividade= pd.read_csv(tbl_atividade, sep=';',encoding='latin-1',dtype=str)
df_atividade.to_sql( 'aux_atividade',engine,if_exists='replace',index=False)
print ('Tabela Atividade enviada')

#-----------------------classe

tbl_classe = os.path.join(diretorio,'Tabela Classe.txt')
df_classe = pd.read_csv(tbl_classe, sep=';',encoding='latin-1',dtype=str)
df_classe.to_sql( 'aux_classe',engine,if_exists='replace',index=False)
print('Tabela Classe enviada')

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


#-----------------------local aposentadoria

tbl_local_aposentadoria = os.path.join(diretorio,'Tabela Local Aposentadoria.txt')
df_local_aposentadoria = pd.read_csv(tbl_local_aposentadoria,sep=';',encoding='latin-1',dtype=str)
df_local_aposentadoria.to_sql('aux_local_aposentadoria',engine,if_exists='replace',index=False)
print('Tabela Local Aposentadoria enviada')



#-----------------------municipio

tbl_municipio = os.path.join(diretorio,'Tabela Municipio.txt')
df_municipio = pd.read_csv(tbl_municipio,sep=';',encoding='latin-1',dtype=str)
df_municipio.to_sql('aux_municipio',engine,if_exists='replace',index=False)
print('Tabela Municipio enviada')

#-----------------------unidade atual

tbl_unidade_atual = os.path.join(diretorio,'Tabela Unidade Atual.txt')
df_unidade_atual = pd.read_csv(tbl_unidade_atual,sep=';',encoding='latin-1',dtype=str)
df_unidade_atual.to_sql('aux_unidade_atual',engine,if_exists='replace',index=False)
print('Tabela Unidade Atual enviada')

#-----------------------uorg endereco

tbl_uorg_endereco = os.path.join(diretorio,'Tabela UORG Endereco.txt')
df_uorg_endereco = pd.read_csv(tbl_uorg_endereco,sep=';',encoding='latin-1',dtype=str)
df_uorg_endereco.to_sql('aux_uorg_endereco',engine,if_exists='replace',index=False)
print('Tabela UORG Endereco enviada')

#-----------------------titulação correção

tbl_titulacao_correcao = os.path.join(diretorio,'Tabela Titulacao Correção.txt')
df_titulacao_correcao = pd.read_csv(tbl_titulacao_correcao,sep=';',encoding='latin-1',dtype=str)
df_titulacao_correcao.to_sql('aux_titulacao_correcao',engine,if_exists='replace',index=False)
print('Tabela Titulação Correção enviada')

#-----------------------titulação correção

tbl_rubrica_incentivo_qualificacao = os.path.join(diretorio,'Tabela Rubrica Incentivo Qualificacao.txt')
df_rubrica_incentivo_qualificacao = pd.read_csv(tbl_rubrica_incentivo_qualificacao,sep=';',encoding='latin-1',dtype=str)
df_rubrica_incentivo_qualificacao.to_sql('aux_rubrica_incentivo_qualificacao',engine,if_exists='replace',index=False)
print('Tabela Rubrica Incentivo Qualificacao enviada')

#-----------------------000_PgtoIcentivoQualificacao

tbl_000_PgtoIcentivoQualificacao = os.path.join(diretorio,'000_PgtoIcentivoQualificacao.txt')
df_000_PgtoIcentivoQualificacao = pd.read_csv(tbl_000_PgtoIcentivoQualificacao,sep=';',encoding='latin-1',dtype=str)
df_000_PgtoIcentivoQualificacao.to_sql('aux_pgtoicentivoqualificacao',engine,if_exists='replace',index=False)
print('000_PgtoIcentivoQualificacao enviada')

