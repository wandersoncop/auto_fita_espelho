import os
import csv
import pandas as pd
from funcoes import *
from conexao import engine
from mapeamentos import (
    LAYOUT_TIPO_1, 
    HEADER_TIPO_1,
    LAYOUT_TIPO_2, 
    HEADER_TIPO_2,
    LAYOUT_TIPO_3, 
    HEADER_TIPO_3,
    LAYOUT_TIPO_4, 
    HEADER_TIPO_4,
    LAYOUT_TIPO_5,
    HEADER_TIPO_5,
    LAYOUT_TIPO_6, 
    HEADER_TIPO_6,
    CAMPOS_DATA_TIPO_1, 
    CAMPOS_DATA_TIPO_2, 
    CAMPOS_DATA_TIPO_3,
    CAMPOS_DATA_TIPO_4, 
    CAMPOS_DATA_TIPO_5, 
    TRADUCAO_DENO_ESCOL,
    TRADUCAO_TIT_FORM,
    TRADUCAO_ESCOLARIDADE,
    TRADUCAO_PAIS,
    TRADUCAO_SIT,
    TRADUCAO_CARGO,    
)

import os
import csv




#---------------- EXECUÇÃO e chamada das tabelas ---

# Identifica automaticamente se o PC é Wanderson, Wandersoncop ou qualquer outro
diretorio = os.path.join(os.path.expanduser("~"), "Desktop", "auto_fita_espelho")

arquivo = 'fita_espelho.txt'
arquivo_insc = 'Pescad_InscUFMG.txt'

tbl_classe = os.path.join(diretorio,'Tabela Classe.txt')
MAPA_CLASSES = carregar_tabela_apoio(tbl_classe, col_chave=0,col_valor=3)

tbl_estado_civil = os.path.join(diretorio,'Tabela Estado Civil.txt')
MAPA_ESTADO_CIVIL = carregar_tabela_apoio(tbl_estado_civil,col_chave=0,col_valor=1)


tbl_atividade = os.path.join(diretorio,'Tabela Atividade.txt')
TRADUCAO_DENOATIV = carregar_tabela_apoio(tbl_atividade,col_chave=2,col_valor=3)

tbl_uorg_endereco = os.path.join(diretorio,'Tabela UORG Endereco.txt')
TRADUCAO_EMAIL = carregar_tabela_apoio(tbl_uorg_endereco,col_chave=16,col_valor=13)

local_ap = os.path.join(diretorio,'Tabela Local Aposentadoria.txt')
TRADUCAO_LOCAL_AP = carregar_tabela_apoio(local_ap,col_chave=0,col_valor=1)

deno_local_ap = os.path.join(diretorio,'Tabela Local Aposentadoria.txt')
TRADUCAO_DENO_LOCAL_AP = carregar_tabela_apoio(deno_local_ap,col_chave=0,col_valor=2)

caminho_municipio = os.path.join(diretorio,'Tabela Municipio.txt')
MAPA_MUNICIPIO = carregar_tabela_apoio(caminho_municipio)
caminho_endereco = os.path.join(diretorio, 'Tabela UORG Endereco.txt')
MAPA_PONTE_MUN = carregar_tabela_apoio(caminho_endereco, col_chave=16, col_valor=3)

caminho_unidade = os.path.join(diretorio,'Tabela Unidade Atual.txt')
MAPA_UNIDADES = carregar_mapa_unidades(caminho_unidade)
# Agora o código usa o diretório dinâmico para carregar os arquivos
mapa_insc = carregar_dicionario_inscricoes(diretorio, arquivo_insc)
caminho_completo = os.path.join(diretorio, arquivo)

# Exemplo de como abrir a Tabela de Estado Civil usando o mesmo diretório
# caminho_estado_civil = os.path.join(diretorio, 'Tabela Estado Civil.txt')

print(f"Diretório detectado: {diretorio}")

# ------------------------------------ PROCESSAMENTO ---
dados_0 = extrair_tipo_0(diretorio, arquivo)

servidores_pessoais,mapa_nomes_aux = extrair_tipo_1(caminho_completo, dados_0,mapa_insc) 
salvar_em_csv(servidores_pessoais, os.path.join(diretorio, 'tipo_1_pessoal.csv')) 

servidores_funcionais = extrair_tipo_2(caminho_completo, dados_0,mapa_insc,mapa_nomes_aux)
salvar_em_csv(servidores_funcionais, os.path.join(diretorio, 'tipo_2_funcional.csv'))

servidores_tipo_3 = extrair_tipo_3(caminho_completo,dados_0)
salvar_em_csv(servidores_tipo_3,os.path.join(diretorio,'tipo_3_registro_pagamento.csv'))

servidores_tipo_4 = extrair_tipo_4(caminho_completo,dados_0)
salvar_em_csv(servidores_tipo_4,os.path.join(diretorio,'tipo_4_totalizador_pagamento.csv'))

servidores_tipo_5 = extrair_tipo_5(caminho_completo,dados_0)
salvar_em_csv(servidores_tipo_5,os.path.join(diretorio,'tipo_5_registro_afastamento.csv'))

servidores_tipo_6 = extrair_tipo_6(caminho_completo,dados_0)
salvar_em_csv(servidores_tipo_6,os.path.join(diretorio,'tipo_6_totalizador_afastamento.csv'))







# ------------------------------------- RELATÓRIO FINAL ---
print("-" * 50)
print(f"PROCESSAMENTO CONCLUÍDO")
print(f"Tipo 1 (Dados Pessoais): {len(servidores_pessoais)} registros extraídos.")
print(f"Tipo 2 (Dados Funcionais): {len(servidores_funcionais)} registros extraídos.")
print(f"Tipo 3 (Registro Pagamentos): {len(servidores_tipo_4)} registros extraídos.")
print(f"Tipo 4 (Totalizador Pagamentos): {len(servidores_tipo_4)} registros extraídos.")
print(f"Tipo 5 (Registro Afastamentos): {len(servidores_tipo_5)} registros extraídos.")
print(f"Tipo 6 (Totalizador Afastamentos): {len(servidores_tipo_6)} registros extraídos.")
print("-" * 50)

print(list(MAPA_MUNICIPIO.items())[:5])

df = pd.DataFrame(servidores_pessoais)

#------------------------------ PARA ENVIAR A TABELA DE TIPO PARA O BANCO SALVAR NO BD


# PASSO 1: Envia os dados "crus" para o MySQL
df.to_sql(
    'tipo_1_pessoal',
    engine,
    if_exists='replace',
    index=False
)

# PASSO 2: Chama a função que criamos no funcoes.py

# Ela vai usar a "receita" que está no arquivo SQL para criar a tabela final
from consulta_sql import QUERY_CONSOLIDACAO_PESSOAL
import funcoes

funcoes.consolidar_dados_pessoal(engine, QUERY_CONSOLIDACAO_PESSOAL)