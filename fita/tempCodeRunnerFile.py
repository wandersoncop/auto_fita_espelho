 elif campo == 'ECIV':
                        dados[campo] = valor
                        dados['DENO_E_CIV'] = TRADUCAO_ESTADO_CIVIL.get(valor, '')
