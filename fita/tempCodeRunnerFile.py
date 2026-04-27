cod_sit = str(dados.get('SIT') or '').zfill(2)
                dados['DENO_SIT'] = TRADUCAO_SIT.get(cod_sit, f'SIT {cod_sit}')