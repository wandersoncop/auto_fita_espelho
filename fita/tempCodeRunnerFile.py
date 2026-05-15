
df_pessoal.to_sql('tipo_1_pessoal',engine,if_exists='replace',index=False)

df_reg_pagamento = pd.DataFrame(servidores_tipo_3)
df_reg_pagamento.to_sql('tipo_3_rg_pagamento',engine,if_exists='replace',index=False)


# Ela vai usar a "receita" que está no arquivo SQL para criar a tabela final
lista_tbl_banco= [
    CRIA_TBL_PESSOAL,
    CRIA_TBL_REGISTRO_PAGAMENTO
    # Se houver mais queries no futuro, basta adicioná-las aqui
]
print('Iniciando a criação de tabelas...')
for query in lista_tbl_banco:
    criar_tbl_banco(engine,query)
print('Processo de craição finalizado')    
