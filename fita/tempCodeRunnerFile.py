def extrair_tipo_2(caminho_arquivo, header, mapa_inscricoes, mapa_nomes):
    lista_dados_funcionais = []
    valor_do_mes = header.get('mes_fita') or header.get('MES_FITA')

    with open(caminho_arquivo, 'r', encoding='latin-1') as f:
        for linha in f:
            # Verifica se a linha tem o tipo 2 na posição 17
            if len(linha) > 18 and linha[17] == '2':
                dados = {'mes_fita': valor_do_mes}
                
                # --- 1. EXTRAÇÃO DO LAYOUT ---
                for campo, (inicio, fim) in LAYOUT_TIPO_2.items():
                    valor = linha[inicio:fim].strip()
                    if not valor:
                        dados[campo] = ""
                    elif campo in CAMPOS_DATA_TIPO_2:
                        dados[campo] = formatar_data(valor)
                    else:
                        dados[campo] = valor

                # 2. CRIAÇÃO DO CAMPO CAT
                gr_cargo = dados.get('GRCARGO', '')
                cat_letra = 'M' if gr_cargo in ('060', '702', '705', '706', '707') else 'T'
                dados['CAT'] = 'Docente' if cat_letra == 'M' else 'Tec-Administrativo'

                # 3. TRADUÇÃO DA CLASSE (DenoClasse)
                val_classe = dados.get('CLASSE') or dados.get('CLAS') or ''
                ref = dados.get('REF') or ''
                primeiro_dig_ref = ref[0] if ref else ""
                chave_final = f"{cat_letra}{val_classe}"

                if gr_cargo == '705' and val_classe == '4' and primeiro_dig_ref != '4':
                    chave_final = f"{cat_letra}{gr_cargo}{val_classe}{primeiro_dig_ref}"

                dados['ChaveClass'] = chave_final
                dados['DenoClasse'] = MAPA_CLASSES.get(chave_final, '') if MAPA_CLASSES else "ERRO: DICIONARIO VAZIO"

#----------------- 4. CODCARGO E TRADUÇÕES (SITUAÇÃO/CARGO)
                v_gr = str(dados.get('GRCARGO', '')).zfill(3)
                v_ca = str(dados.get('CARGO', '')).zfill(3)
                dados['CodCargo'] = v_gr + v_ca
                
                cod_sit = str(dados.get('SIT') or '').zfill(2)
                dados['DENO_SIT'] = TRADUCAO_SIT.get(cod_sit, f'SIT {cod_sit}')
                
                cod_cargo_full = dados['CodCargo'].zfill(6)
                dados['DENOCARG'] = TRADUCAO_CARGO.get(cod_cargo_full, f'DENOCARG {cod_cargo_full}')

                # 5. MATRICULA E NOME
                matric_func = str(dados.get('MATRIC', '')).strip()
                dados['NOME'] = mapa_nomes.get(matric_func, 'NOME NAO ENCONTRADO')
                dados['InscUFMG'] = mapa_inscricoes.get(matric_func, '')

                # 6. REGRA DO RT
                valor_rtrab = dados.get('RTRAB','').strip()
                dados['RT'] = 'DE' if valor_rtrab == '99' else valor_rtrab

                # --- 7. TRADUÇÃO DA UNIDADE (TABELA EXTERNA) ---
                # Pega o código da fita (ex: 000002769)
                valor_fita = dados.get('NrUorgLotacao', '').strip()
                
                # Busca no mapa (que agora está sem aspas)
                unidade_info = MAPA_UNIDADES.get(valor_fita)

                if isinstance(unidade_info, dict):
                    # Pega os nomes exatos das colunas da sua tabela
                    dados['UnidLotacao'] = unidade_info.get('Unid', '')
                    dados['DenoSetorLotacao'] = unidade_info.get('DenoSetor', '')
                else:
                    dados['UnidLotacao'] = ''
                    dados['DenoSetorLotacao'] = ''

#-----------------------------DEFINIÇÃO PARA O CAMPO TEM FUNÇÃO-------------------------------------
                
                # --- AJUSTE DA LOGICA BASEADO NO DEBUG ---

                # 1. Capturamos os valores (como você já fez)
                gr_exc = dados.get('GREXC','').strip()
                sit    = dados.get('SIT','').strip()
                fun    = dados.get('FUN','').strip()
                dt_fim = dados.get('DtChefFim','').strip()

                # 2. A Nova Regra (mais flexível com as datas e formatos)
                # Note que agora testamos '00000000' OU '00/00/0000' OU vazio ''
                if (gr_exc == '00' and 
                    sit != '02' and 
                    fun != '' and 
                    (dt_fim == '00000000' or dt_fim == '00/00/0000' or dt_fim == '') and 
                    fun != 'ETG'):
                    
                    dados['TemFuncao'] = 'S'
                else:
                    dados['TemFuncao'] = 'N'
                    
#-----------------------------DEFINIÇÃO PARA O CAMPO FUNCSETOR-------------------------------------
               
                nov_fun_sigl = dados.get('NOVFUNCSIGLA','').strip()
                nov_fun_unor = dados.get('NOVFUNCUNORG','').strip()
                fun_unorg =  dados.get('FUNUNORG','').strip()

                if nov_fun_sigl != '':
                    func_setor = nov_fun_unor
                else:
                    func_setor =  fun_unorg
                dados['FuncSetor'] = func_setor       



#------------------------------ 8. MONTAGEM FINAL PARA O CSV ---
                try:
                    dados_ordenado = {campo: dados.get(campo) for campo in HEADER_TIPO_2}
                    lista_dados_funcionais.append(dados_ordenado)
                except Exception as e:
                    print(f"Erro de mapeamento no Header: {e}")
                
    return lista_dados_funcionais