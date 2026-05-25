import pandas as pd
from funcoes import *
from conexao import engine
from consulta_sql import(
    CRIA_TBL_PESSOAL,
    CRIA_TBL_FUNCIONAL,
    CRIA_TBL_REGISTRO_PAGAMENTO,
    CRIA_TBL_PGTO_INCENTIVO_QUALIFICACAO,
    # COLOQUE AS TABELAS QUE NECESSITAR
) 
    

from consulta_sql import QUERY_LIMPEZA_TEMPORARIOS
from mapeamentos import (
    LAYOUT_TIPO_1, HEADER_TIPO_1,CAMPOS_DATA_TIPO_1, 
    LAYOUT_TIPO_2, HEADER_TIPO_2, CAMPOS_DATA_TIPO_2, 
    LAYOUT_TIPO_3, HEADER_TIPO_3,CAMPOS_DATA_TIPO_3,
    LAYOUT_TIPO_4, HEADER_TIPO_4,CAMPOS_DATA_TIPO_4, 
    LAYOUT_TIPO_5, HEADER_TIPO_5,CAMPOS_DATA_TIPO_5, 
    LAYOUT_TIPO_6, HEADER_TIPO_6
)

import os
import csv




#---------------- EXECUÇÃO e chamada das tabelas ---

# Identifica automaticamente se o PC é Wanderson, Wandersoncop ou qualquer outro
diretorio = os.path.join(os.path.expanduser("~"), "Desktop", "auto_fita_espelho")

arquivo = 'fita_espelho.txt'
arquivo_insc = 'Pescad_InscUFMG.txt'



mapa_insc = carregar_dicionario_inscricoes(diretorio, arquivo_insc)
caminho_completo = os.path.join(diretorio, arquivo)


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




# ------------------------------------- RELATÓRIO FINAL  ---
print("-" * 50)
print("PROCESSAMENTO CONCLUÍDO")
print(f"Tipo 1 (Dados Pessoais): {len(servidores_pessoais)} registros extraídos.")
print(f"Tipo 2 (Dados Funcionais): {len(servidores_funcionais)} registros extraídos.")
print(f"Tipo 3 (Registro Pagamentos): {len(servidores_tipo_3)} registros extraídos.")
print(f"Tipo 4 (Totalizador Pagamentos): {len(servidores_tipo_4)} registros extraídos.")
print(f"Tipo 5 (Registro Afastamentos): {len(servidores_tipo_5)} registros extraídos.")
print(f"Tipo 6 (Totalizador Afastamentos): {len(servidores_tipo_6)} registros extraídos.")
print("-" * 50)


df_pessoal = pd.DataFrame(servidores_pessoais)
df_pessoal.to_sql('tipo_1_pessoal',engine,if_exists='replace',index=False)

df_funcional = pd.DataFrame(servidores_funcionais)
df_funcional.to_sql('tipo_2_funcional',engine,if_exists='replace',index=False)

df_reg_pagamento = pd.DataFrame(servidores_tipo_3)
df_reg_pagamento.to_sql('tipo_3_rg_pagamento',engine,if_exists='replace',index=False)


# Ela vai usar a o arquivo consulta_sql.py para criar a tabela final
lista_tbl_banco= [
    CRIA_TBL_PESSOAL,
    CRIA_TBL_FUNCIONAL,
    CRIA_TBL_PGTO_INCENTIVO_QUALIFICACAO,
    CRIA_TBL_REGISTRO_PAGAMENTO,
    # Se houver mais queries no futuro, basta adicioná-las aqui
]
print('Iniciando a criação de tabelas...')
for query in lista_tbl_banco:
    criar_tbl_banco(engine,query)
print('Processo de craição finalizado')    
