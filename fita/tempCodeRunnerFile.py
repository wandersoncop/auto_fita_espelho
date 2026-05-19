servidores_tipo_3 = extrair_tipo_3(caminho_completo,dados_0)
salvar_em_csv(servidores_tipo_3,os.path.join(diretorio,'tipo_3_registro_pagamento.csv'))

servidores_tipo_4 = extrair_tipo_4(caminho_completo,dados_0)
salvar_em_csv(servidores_tipo_4,os.path.join(diretorio,'tipo_4_totalizador_pagamento.csv'))

servidores_tipo_5 = extrair_tipo_5(caminho_completo,dados_0)
salvar_em_csv(servidores_tipo_5,os.path.join(diretorio,'tipo_5_registro_afastamento.csv'))

servidores_tipo_6 = extrair_tipo_6(caminho_completo,dados_0)
sal