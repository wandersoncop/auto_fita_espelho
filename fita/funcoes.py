import os
import csv
import pandas as pd
from sqlalchemy import text 
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
)

def carregar_dicionario_inscricoes(fita, Pescad_InscUFMG):
    caminho = os.path.join(fita, Pescad_InscUFMG)
    mapa_inscricoes = {}
    try:
        # Supondo que as colunas no seu txt sejam MATRIC e InscUFMG separadas por ';'
        df_insc = pd.read_csv(caminho, sep=';', encoding='latin-1', dtype=str)
        
        # Criamos um dicionário onde a chave é a matrícula e o valor é a inscrição
        # .strip() remove espaços em branco acidentais
        mapa_inscricoes = dict(zip(df_insc['MATRIC'].str.strip(), df_insc['InscUFMG'].str.strip()))
    except Exception as e:
        print(f"Erro ao carregar arquivo de inscrições: {e}")
    return mapa_inscricoes

def formatar_data(valor):
    if valor and len(valor) == 8 and valor.isdigit():
        return f'{valor[0:2]}/{valor[2:4]}/{valor[4:8]}'
    return valor

def extrair_tipo_0(fita, fita_espelho):
    caminho_arquivo = os.path.join(fita, fita_espelho)
    header = {
        "tipo": None,
        "codigo_orgao": None,
        "sigla_orgao": None,
        "mes_fita": "0000_00" # Valor padrão caso não ache
    }
    
    with open(caminho_arquivo, 'r', encoding='latin-1') as f:
        for linha in f:
            # A linha de Header oficial do SIAPE começa com '0' na posição 17
            if len(linha) > 18 and linha[17] == '0':
                mes_bruto = linha[45:51].strip()
                
                if len(mes_bruto) == 6:
                    mes = mes_bruto[0:2]
                    ano = mes_bruto[2:6]
                    mes_fita_final = f"{ano}_{mes}"
                else:
                    mes_fita_final = mes_bruto
                
                header = {
                    "tipo": '0',
                    "codigo_orgao": linha[30:35].strip(),
                    "sigla_orgao": linha[35:45].strip(),
                    "mes_fita": mes_fita_final
                }
                print(f"SUCESSO: Header encontrado! Mês: {mes_fita_final}")
                return header
                
    print("AVISO: Linha Tipo 0 não encontrada no arquivo! Usando valores vazios.")
    return header

def extrair_tipo_1(caminho_arquivo, header, mapa_inscricoes):
    lista_dados_pessoais = []
    # aqui vais guardar os nomes para usar em outras tabelas
    mapa_nomes = {} # Dicionário auxiliar: { matricula: nome }
    # Pega o valor do mês uma única vez aqui fora para garantir
    valor_do_mes = header.get('mes_fita') or header.get('MES_FITA')
    
    with open(caminho_arquivo, 'r', encoding='latin-1') as f:
        for linha in f:
            if len(linha) > 18 and linha[17] == '1':
                dados = {}
                
                # 1. Extração do layout com FORMATAÇÃO DE DATA integrada
                for campo, (inicio, fim) in LAYOUT_TIPO_1.items():
                    valor = linha[inicio:fim].strip()
                    if not valor:
                        dados[campo] = None
                    elif campo in CAMPOS_DATA_TIPO_1:
                        # Reinsere a chamada da função que formata DD/MM/AAAA
                        dados[campo] = formatar_data(valor)
                    else:
                        dados[campo] = valor

                # 2. Fixação de campos externos e cálculos
                dados['mes_fita'] = valor_do_mes 
                matric_limpa = str(linha[9:16]).strip() # Posição da matrícula no texto
                nome_servidor = str(linha[20:80]).strip() # Posição do nome no Tipo 1

                dados['MATRIC'] = matric_limpa
                dados ['NOME'] = nome_servidor
                dados['InscUFMG'] = mapa_inscricoes.get(matric_limpa,'')
                # Inscrição UFMG
                matric_limpa = str(dados.get('MATRIC', '')).strip()
                dados['InscUFMG'] = mapa_inscricoes.get(matric_limpa, '')
                # Alimenta o mapa de nomes para usar no Tipo 2
                mapa_nomes[matric_limpa] = nome_servidor   
                
              # 3. Montagem final conforme a ordem do HEADER_TIPO_1
                dados_ordenado = {campo: dados.get(campo) for campo in HEADER_TIPO_1}
                lista_dados_pessoais.append(dados_ordenado)




             
                
    return lista_dados_pessoais, mapa_nomes

def extrair_tipo_2(caminho_arquivo, header, mapa_inscricoes, mapa_nomes):
    lista_dados_funcionais = []
    valor_do_mes = header.get('mes_fita') or header.get('MES_FITA')

    with open(caminho_arquivo, 'r', encoding='latin-1') as f:
        for linha in f:
            # Verifica se a linha tem o tipo 2 na posição 17
            if len(linha) > 18 and linha[17] == '2':
                dados = {'mes_fita': valor_do_mes}
                
#---------------------------------------- 1. EXTRAÇÃO DO LAYOUT ---
                for campo, (inicio, fim) in LAYOUT_TIPO_2.items():
                    valor = linha[inicio:fim].strip()
                    if not valor:
                        dados[campo] = ""
                    elif campo in CAMPOS_DATA_TIPO_2:
                        dados[campo] = formatar_data(valor)
                    else:
                        dados[campo] = valor

#---------------------------------------- 2. CRIAÇÃO DO CAMPO CAT ---
                gr_cargo = dados.get('GRCARGO', '')
                cat_letra = 'M' if gr_cargo in ('060', '702', '705', '706', '707') else 'T'
                dados['CAT'] = 'Docente' if cat_letra == 'M' else 'Tec-Administrativo'

                # --- 3. TRADUÇÃO DA CLASSE (DenoClasse) ---
                val_classe = dados.get('CLASSE') or dados.get('CLAS') or ''
                ref = dados.get('REF') or ''
                primeiro_dig_ref = ref[0] if ref else ""
                chave_final = f"{cat_letra}{val_classe}"

                if gr_cargo == '705' and val_classe == '4' and primeiro_dig_ref != '4':
                    chave_final = f"{cat_letra}{gr_cargo}{val_classe}{primeiro_dig_ref}"

                dados['ChaveClass'] = chave_final
                # dados['DenoClasse'] = MAPA_CLASSES.get(chave_final, '') if MAPA_CLASSES else "ERRO: MAPA VAZIO"

                # --- 4. CODCARGO E TRADUÇÕES (SITUAÇÃO/CARGO) ---
                v_gr = str(dados.get('GRCARGO', '')).zfill(3)
                v_ca = str(dados.get('CARGO', '')).zfill(3)
                dados['CodCargo'] = v_gr + v_ca
                
                # cod_sit = str(dados.get('SIT') or '').zfill(2)
                # dados['DENO_SIT'] = TRADUCAO_SIT.get(cod_sit, f'SIT {cod_sit}')
                
                # cod_cargo_full = dados['CodCargo'].zfill(6)
                # dados['DENOCARG'] = TRADUCAO_CARGO.get(cod_cargo_full, f'DENOCARG {cod_cargo_full}')

                # --- 5. MATRICULA E NOME ---
                matric_func = str(dados.get('SIAPE', '')).strip()
                dados['Nome'] = mapa_nomes.get(matric_func, 'NOME NAO ENCONTRADO')
                dados['InscUFMG'] = mapa_inscricoes.get(matric_func, '')

#---------------------------------------- 6. REGRA DO RT ---
                valor_rtrab = dados.get('RTRAB','').strip()
                dados['RT'] = 'DE' if valor_rtrab == '99' else valor_rtrab

# #----------------------------------------7. TRADUÇÃO DA UNIDADE DE LOTAÇÃO ---
#                 uorg_lotacao = dados.get('NrUorgLotacao', '').strip()
#                 unidade_lot_info = MAPA_UNIDADES.get(uorg_lotacao)

#                 if isinstance(unidade_lot_info, dict):
#                     dados['UnidLotacao'] = unidade_lot_info.get('Unid', '')
#                     dados['DenoSetorLotacao'] = unidade_lot_info.get('DenoSetor', '')
#                     dados['UorgPaiExercicio'] = unidade_lot_info.get('UorgPai','').strip()
#                     dados['NomeUorgPaiExercicio'] = unidade_lot_info.get('NomeUorgPai','').strip()
#                 else:
#                     dados['UnidLotacao'] = ''
#                     dados['DenoSetorLotacao'] = ''
#                     dados['UorgPaiExercicio'] = ''
#                     dados['NomeUorgPaiExercicio'] = ''

#---------------------------------------- 8. DEFINIÇÃO DO CAMPO TEMFUNCAO ---
             
                dados['TemFuncao'] = calcular_tem_funcao(dados)

#------------------------------------------- 9. DEFINIÇÃO DO CAMPO FUNCSETOR ---
                nov_fun_sigl = dados.get('NOVFUNCSIGLA','').strip()
                nov_fun_unor = dados.get('NOVFUNCUNORG','').strip()
                fun_unorg    = dados.get('FUNCUNORG','').strip()

                if nov_fun_sigl != '' and nov_fun_unor != '000000000':
                    func_setor = nov_fun_unor
                else:
                    func_setor = fun_unorg
                
                dados['FuncSetor'] = func_setor
                
#----------------------------------------10. DEFINIÇÃO DO NrUorgExercicio ---
                # rj = dados.get('RJ', '').strip()

                # if (rj == "ETG" and func_setor != "000000000" and func_setor != "") or dados.get('TemFuncao') == "S":
                #     exercicio_final = func_setor
                # else:
                #     exercicio_final = uorg_lotacao

                # dados['NrUorgExercicio'] = exercicio_final
                

#---------------------------------------- 11. TRADUÇÃO DA UNIDADE DE EXERCÍCIO ---
                # unidade_ex_info = MAPA_UNIDADES.get(exercicio_final)

                # if isinstance(unidade_ex_info, dict):
                #     dados['UnidExercicio'] = unidade_ex_info.get('Unid', '')
                #     dados['DenoSetorExercicio'] = unidade_ex_info.get('DenoSetor', '')
                #     dados['UnidFunc'] = unidade_ex_info.get('Unid', '')
                #     dados['DenoSetorFunc'] = unidade_ex_info.get('DenoSetor', '')
                # else:
                #     dados['UnidExercicio'] = ''
                #     dados['DenoSetorExercicio'] = ''
                #     dados['UnidFunc'] =''
                #     dados['DenoSetorFunc'] = ''


#---------------------------------------- 12. TRADUÇÃO DE DENOATIV --- 

            # Tradução de DENOATIV
                # dados['DENOATIV'] = TRADUCAO_DENOATIV.get(str(dados.get('ATIVFUNC')).zfill(4), '')
#---------------------------------------- 13. TRADUÇÃO DE email --- 

            # Tradução de email uorg
                # dados['EmailUORGExercicio'] = TRADUCAO_EMAIL.get(str(dados.get('NrUorgLotacao')).zfill(9), '')
            
            # Tradução de NrUorgLocalAP
                # dados['NrUorgLocalAP'] = TRADUCAO_LOCAL_AP.get(str(dados.get('MATRIC')).zfill(7), '')
                # dados['DenoSetorLocalAP'] = TRADUCAO_DENO_LOCAL_AP.get(str(dados.get('MATRIC')).zfill(7), '')

#------------------------------------- 14 Tradução de municipio
                # Aqui usamos a variável 'exercicio_final' que você já criou no seu passo 10
                # dados['MunicipioUORGExercicio'] = buscar_municipio_isolado(exercicio_final, MAPA_PONTE_MUN, MAPA_MUNICIPIO)



#---------------------------------------- 15 MONTAGEM FINAL PARA O CSV ---
                try:
                    # Filtra apenas as colunas que estão no seu HEADER_TIPO_2 (mapeamentos.py)
                    dados_ordenado = {campo: dados.get(campo, '') for campo in HEADER_TIPO_2}
                    lista_dados_funcionais.append(dados_ordenado)
                except Exception as e:
                    print(f"Erro ao organizar dados para o CSV: {e}")

    return lista_dados_funcionais

def extrair_tipo_3(caminho_arquivo, header):
    lista_tipo_3 = [] 
    valor_do_mes = header.get('mes_fita')

    with open(caminho_arquivo, 'r', encoding='latin-1') as f:
        for linha in f:
            # Verifica se a linha tem tamanho suficiente e se é tipo 4
            if len(linha) > 18 and linha[17] == '3':
                dados = {'mes_fita': valor_do_mes} # Variável criada aqui
                
                # O loop de extração DEVE estar alinhado com o dicionário 'dados'
                for campo, (inicio, fim) in LAYOUT_TIPO_3.items():
                    valor = linha[inicio:fim].strip()
                    if not valor:
                        dados[campo] = None
                    elif campo in CAMPOS_DATA_TIPO_3:
                        dados[campo] = formatar_data(valor)
                    else:
                        dados[campo] = valor
                
    
                lista_tipo_3.append(dados)

           
                
    return lista_tipo_3  

def extrair_tipo_4(caminho_arquivo, header):
    lista_tipo_4 = [] 
    valor_do_mes = header.get('mes_fita')

    with open(caminho_arquivo, 'r', encoding='latin-1') as f:
        for linha in f:
            # Verifica se a linha tem tamanho suficiente e se é tipo 4
            if len(linha) > 18 and linha[17] == '4':
                dados = {'mes_fita': valor_do_mes} # Variável criada aqui
                
                # O loop de extração DEVE estar alinhado com o dicionário 'dados'
                for campo, (inicio, fim) in LAYOUT_TIPO_4.items():
                    valor = linha[inicio:fim].strip()
                    if not valor:
                        dados[campo] = None
                    elif campo in CAMPOS_DATA_TIPO_4:
                        dados[campo] = formatar_data(valor)
                    else:
                        dados[campo] = valor
                
                # O append também deve estar dentro do IF, para salvar apenas o tipo 4
                lista_tipo_4.append(dados)
                
    return lista_tipo_4                               

def extrair_tipo_5(caminho_arquivo,header):
    lista_tipo_5 = []
    valor_do_mes = header.get('mes_fita')
    
    with open(caminho_arquivo,'r',encoding='latin-1') as f:
        for linha in f:
            if len(linha)>18 and linha[17]=='5':
                dados = {'mes_fita':valor_do_mes}                
              # 1. Extração do layout com FORMATAÇÃO DE DATA integrada  
                for campo,(inicio,fim)in LAYOUT_TIPO_5.items():
                    valor=linha[inicio:fim].strip()
                    if not valor:
                        dados[campo]=None
                    elif campo in CAMPOS_DATA_TIPO_5:
                        dados[campo]=formatar_data(valor)
                    else:
                        dados[campo] = valor
                    
                lista_tipo_5.append(dados) 

                       
    return lista_tipo_5  

def extrair_tipo_6(caminho_arquivo, header):
    lista_tipo_6 = []
    # Pegamos o mês do header (Tipo 0) para o dado não ficar 'solto' no tempo
    valor_do_mes = header.get('mes_fita')
    
    with open(caminho_arquivo, 'r', encoding='latin-1') as f:
        for linha in f:
            # Verifica se a linha tem o tipo 6 na posição 17 (índice 17 é a 18ª posição)
            if len(linha) > 18 and linha[17] == '6': 
                dados = {'mes_fita': valor_do_mes}
                
                # Percorre o layout que você definiu no mapeamentos.py
                for campo, (inicio, fim) in LAYOUT_TIPO_6.items():
                    valor = linha[inicio:fim].strip()
                    dados[campo] = valor
                
                
                lista_tipo_6.append(dados)
                
    return lista_tipo_6 

def calcular_tem_funcao(dados):
    # 1. Pegamos os valores e forçamos a limpeza de espaços
    # Usamos o .get() com fallback para string vazia para evitar erros
    gr  = str(dados.get('GREXC', '')).strip()
    sit = str(dados.get('SIT', '')).strip()
    fun = str(dados.get('FUN', '')).strip()
    

    dt_fim = ""
    for chave, valor in dados.items():
        if 'DtChefFim' in chave:
            dt_fim = str(valor).strip()
            break

    
    c1 = (gr == '00' or gr == '0')
    c2 = (sit != '02')
    c3 = (fun != '' and fun != 'ETG')
    c4 = (dt_fim == '00000000' or dt_fim == '00/00/0000' or dt_fim == '')

    if c1 and c2 and c3 and c4:
        return 'S'
    
    return 'N'

def salvar_em_csv(lista_dados, nome_arquivo):
    if not lista_dados:
        print(f'Aviso: Lista para {nome_arquivo} está vazia.')    
        return
    colunas = lista_dados[0].keys()
    with open(nome_arquivo, 'w', newline='', encoding='latin-1') as f:
        escritor = csv.DictWriter(f, fieldnames=colunas, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL,lineterminator='\r\n')
        escritor.writeheader()
        escritor.writerows(lista_dados)
    print(f'Arquivo salvo: {nome_arquivo}') 


from sqlalchemy import text





def criar_tbl_banco(engine, query_sql):
    """
    cria as tabelas finais no banco de dados

    Args:
        engine: Objeto de conexão SQLAlchemy
        query_sql (str): String contendo uma ou mais consultas SQL separadas por ';'
    """
    try:
        with engine.begin() as conexao:
            for comando in query_sql.split(";"):
                comando_limpo = comando.strip()
                if comando_limpo:  # Evita executar strings vazias
                    conexao.execute(text(comando_limpo))
            
            print("✅ CONSOLIDAÇÃO CONCLUÍDA COM SUCESSO!")

    except Exception as erro:
        print(f"❌ ERRO CRÍTICO NA CONSOLIDAÇÃO: {erro}")