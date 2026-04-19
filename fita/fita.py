import os
import csv
from mapeamentos import (
    LAYOUT_TIPO_1, 
    LAYOUT_TIPO_2, 
    CAMPOS_DATA_TIPO_1, 
    CAMPOS_DATA_TIPO_2, 
    TRADUCAO_ESTADO_CIVIL
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
                
                for campo, (inicio, fim) in LAYOUT_TIPO_1.items():
                    valor = linha[inicio:fim].strip()
                    if not valor:
                        dados[campo] = None
                    elif campo in CAMPOS_DATA_TIPO_1:
                        dados[campo] = formatar_data(valor)
                    elif campo == 'estado_civil':
                        dados[campo] = valor
                        dados['estado_civil_desc'] = TRADUCAO_ESTADO_CIVIL.get(valor, '')
                    else:
                        dados[campo] = valor
                lista_dados_pessoais.append(dados)    
    return lista_dados_pessoais 

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
diretorio = r'c:\Users\Wanderson\Desktop\auto_fita_espelho'
arquivo = 'fita_espelho.txt'
caminho_completo = os.path.join(diretorio, arquivo)

# Processamento
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