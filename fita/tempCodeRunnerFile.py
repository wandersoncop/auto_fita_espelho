

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
print("PROCESSAMENTO CONCLUÍDO")
print(f"Tipo 1 (Dados Pessoais): {len(servidores_pessoais)} registros extraídos.")
print(f"Tipo 2 (Dados Funcionais): {len(servidores_funcionais)} registros extraídos.")
print(f"Tipo 3 (Registro Pagamentos): {len(servidores_tipo_3)} registros extraídos.")
print(f"Tipo 4 (Totalizador Pagamentos): {len(servidores_tipo_4)} registros extraídos.")
print(f"Tipo 5 (Registro Afastamentos): {len(servidores_tipo_5)} registros extraídos.")
print(f"Tipo 6 (Totalizador Afastamentos): {len(servidores_tipo_6)} registros extraídos.")
print("-" * 50)

# print(list(MAPA_MUNICIPIO.items())[:5])

df = pd.DataFrame(servidores_pessoais)

#------------------------------ PARA ENVIAR A TABELA DE TIPO PARA O BANCO SALVAR NO BD


# PASSO 1: Envia os dados "crus" para o MySQL
df.to_sql(
    'tipo_1_pessoal',
    engine,
    if_exists='replace',
    index=False
)


# Ela vai usar a "receita" que está no arquivo SQL para criar a tabela final
criar_tbl_pessoal(engine, QUERY_CONSOLIDACAO_PESSOAL)