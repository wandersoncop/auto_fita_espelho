def extrair_tipo_1(caminho_arquivo, header,mapa_inscricoes):
    lista_dados_pessoais = []
    with open(caminho_arquivo, 'r', encoding='latin-1') as f:
        for linha in f:
            if len(linha) > 18 and linha[17] == '1':
                dados = {'mes_fita': header['mes_fita']}
                
               # --- DENTRO DA FUNÇÃO extrair_tipo_1 ---

                for campo, (inicio, fim) in LAYOUT_TIPO_1.items():
                    valor = linha[inicio:fim].strip()
                    if not valor:
                        dados[campo] = None
                    elif campo in CAMPOS_DATA_TIPO_1:
                        dados[campo] = formatar_data(valor)
                    
                    elif campo == 'ECIV':
                        dados[campo] = valor
                        dados['DENO_E_CIV'] = TRADUCAO_ESTADO_CIVIL.get(valor, '')

                    # AJUSTE AQUI: O nome no seu LAYOUT_TIPO_1 é 'ESCOL'
                    elif campo == 'ESCOL':
                        dados['COD_ESCOL'] = valor # Guardamos como COD_ESCOL para a função calcular
                        valor_str = str(valor).zfill(2)
                        dados['DENO_ESCOL'] = TRADUCAO_DENO_ESCOL.get(valor_str, '')
                    
                    # AJUSTE AQUI: O nome no seu LAYOUT_TIPO_1 é 'TIT_FORM'
                    elif campo == 'TIT_FORM':
                        dados['COD_TITULACAO'] = valor # Guardamos como COD_TITULACAO para a função calcular
                        valor_str = str(valor).zfill(2)
                        dados['DENO_TIT'] = TRADUCAO_TIT_FORM.get(valor_str, '')
                                            
                    elif campo == 'PAIS':
                        dados[campo] = valor
                        valor_str = str(valor).zfill(3) # Países costumam ter 3 dígitos (ex: 024)
                        dados['DENO_PAIS'] = TRADUCAO_PAIS.get(valor_str, '')

                    else:
                        dados[campo] = valor

                #BUSCA A INCRICAO UFMG
                matric_limpa = str(dados.get('MATRIC','')).strip()
                dados['InscUFMG'] = mapa_inscricoes.get(matric_limpa,'')

                # Agora a função calcular_escolaridade 
                dados['ESCOLARIDADE'] = calcular_escolaridade(dados)
                    #  FAZ A ORGANIZAÇÃO DE SAIDA DAS COLUNAS DA TABELA
                dados_ordenado = {campo: dados.get(campo) for campo in HEADER_TIPO_1}
                lista_dados_pessoais.append(dados_ordenado)

                        

               
    return lista_dados_pessoais 