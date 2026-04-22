import os
import csv
import pandas as pd
from mapeamentos import (
    LAYOUT_TIPO_1, 
    HEADER_TIPO_1,
    LAYOUT_TIPO_2, 
    CAMPOS_DATA_TIPO_1, 
    CAMPOS_DATA_TIPO_2, 
    TRADUCAO_ESTADO_CIVIL,
    TRADUCAO_DENO_ESCOL,
    TRADUCAO_TIT_FORM,
    TRADUCAO_ESCOLARIDADE,
    TRADUCAO_PAIS,
)

def formatar_data(valor):
    if valor and len(valor) == 8 and valor.isdigit():
        return f'{valor[0:2]}/{valor[2:4]}/{valor[4:8]}'
    return valor

def extrair_tipo_0(fita, fita_espelho):
    caminho_arquivo = os.path.join(fita, fita_espelho)
    with open(caminho_arquivo, 'r', encoding='latin-1') as f:
        linha0 = f.readline()
        mes_bruto = linha0[45:51].strip()
        
        if len(mes_bruto) == 6:
            mes = mes_bruto[0:2]
            ano = mes_bruto[2:6]
            mes_fita_final = f"{ano}_{mes}"
        else:
            mes_fita_final = mes_bruto 
            
        header = {
            "tipo": linha0[17:18],
            "codigo_orgao": linha0[30:35].strip(),
            "sigla_orgao": linha0[35:45].strip(),
            "mes_fita": mes_fita_final
        }
        return header

def extrair_tipo_1(caminho_arquivo, header):
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

                # Agora a função calcular_escolaridade vai encontrar os dados
                dados['ESCOLARIDADE'] = calcular_escolaridade(dados)
                    #  FAZ A ORGANIZAÇÃO DE SAIDA DAS COLUNAS DA TABELA
                dados_ordenado = {campo: dados.get(campo) for campo in HEADER_TIPO_1}
                lista_dados_pessoais.append(dados_ordenado)

                        

               
    return lista_dados_pessoais 

def calcular_escolaridade(dados):
    cod_escol = str(dados.get('COD_ESCOL', '')).zfill(2)
    cod_tit = str(dados.get('COD_TITULACAO','')).zfill(2)

    grau_escol = TRADUCAO_ESCOLARIDADE.get(cod_escol,-1)
    grau_tit = TRADUCAO_ESCOLARIDADE.get(cod_tit,-1)

    deno_escol = dados.get('DENO_ESCOL','')
    deno_tit = dados.get('DENO_TIT','')

    if grau_escol >= 0 and grau_tit >=0:
        return deno_escol if grau_escol >=grau_tit else deno_tit

    if grau_tit >= 0:
        return deno_tit
   
    if grau_escol >= 0:
        return deno_escol
    
    return ''



 


def extrair_tipo_2(caminho_arquivo, header):
    lista_dados_funcionais = []
    with open(caminho_arquivo, 'r', encoding='latin-1') as f:
        for linha in f:
            if len(linha) > 18 and linha[17] == '2':
                dados = {'mes_fita': header['mes_fita']}
                for campo, (inicio, fim) in LAYOUT_TIPO_2.items():
                    valor = linha[inicio:fim].strip()
                    if not valor:
                        dados[campo] = None
                    elif campo in CAMPOS_DATA_TIPO_2:
                        dados[campo] = formatar_data(valor)
                    else:
                        dados[campo] = valor
                lista_dados_funcionais.append(dados)
    return lista_dados_funcionais       

def salvar_em_csv(lista_dados, nome_arquivo):
    if not lista_dados:
        print(f'Aviso: Lista para {nome_arquivo} está vazia.')    
        return
    colunas = lista_dados[0].keys()
    with open(nome_arquivo, 'w', newline='', encoding='latin-1') as f:
        escritor = csv.DictWriter(f, fieldnames=colunas, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        escritor.writeheader()
        escritor.writerows(lista_dados)
    print(f'Arquivo salvo: {nome_arquivo}')       

# --- EXECUÇÃO ---
diretorio = r'c:\Users\Wandersoncop\Desktop\auto_fita_espelho'
arquivo = 'fita_espelho.txt'
caminho_completo = os.path.join(diretorio, arquivo)

# --- PROCESSAMENTO ---
dados_0 = extrair_tipo_0(diretorio, arquivo)

servidores_pessoais = extrair_tipo_1(caminho_completo, dados_0) 
salvar_em_csv(servidores_pessoais, os.path.join(diretorio, 'servidores_tipo1_pessoal.csv')) 

servidores_funcionais = extrair_tipo_2(caminho_completo, dados_0)
salvar_em_csv(servidores_funcionais, os.path.join(diretorio, 'servidores_tipo2_funcional.csv'))

# --- RELATÓRIO FINAL ---
print("-" * 50)
print(f"PROCESSAMENTO CONCLUÍDO")
# len(servidores_pessoais) conta quantos itens existem na lista do Tipo 1
print(f"Tipo 1 (Dados Pessoais): {len(servidores_pessoais)} registros extraídos.")
# len(servidores_funcionais) conta quantos itens existem na lista do Tipo 2
print(f"Tipo 2 (Dados Funcionais): {len(servidores_funcionais)} registros extraídos.")
print("-" * 50)

df = pd.DataFrame(servidores_pessoais)