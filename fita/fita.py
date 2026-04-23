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
                
                # Inscrição UFMG
                matric_limpa = str(dados.get('MATRIC', '')).strip()
                dados['InscUFMG'] = mapa_inscricoes.get(matric_limpa, '')
                
                # Estado Civil
                dados['DENO_E_CIV'] = TRADUCAO_ESTADO_CIVIL.get(dados.get('ECIV'), '')
                
                # Preparação para Escolaridade
                dados['COD_ESCOL'] = str(dados.get('ESCOL', '')).zfill(2)
                dados['COD_TITULACAO'] = str(dados.get('TIT_FORM', '')).zfill(2)

                # Traduções de escolaridade e título
                dados['DENO_ESCOL'] = TRADUCAO_DENO_ESCOL.get(dados['COD_ESCOL'], '')
                dados['DENO_TIT'] = TRADUCAO_TIT_FORM.get(dados['COD_TITULACAO'], '')
                
                # Cálculo do maior grau
                dados['ESCOLARIDADE'] = calcular_escolaridade(dados)
                
                # Tradução de País
                dados['DENO_PAIS'] = TRADUCAO_PAIS.get(str(dados.get('PAIS')).zfill(3), '')

                # 3. Montagem final conforme a ordem do HEADER_TIPO_1
                dados_ordenado = {campo: dados.get(campo) for campo in HEADER_TIPO_1}
                lista_dados_pessoais.append(dados_ordenado)
                
    return lista_dados_pessoais

def calcular_escolaridade(dados):
    # Tenta pegar pelo nome novo ou pelo nome bruto do layout
    cod_escol = str(dados.get('COD_ESCOL') or dados.get('ESCOL') or '').strip().zfill(2)
    cod_tit = str(dados.get('COD_TITULACAO') or dados.get('TIT_FORM') or '').strip().zfill(2)

    grau_escol = TRADUCAO_ESCOLARIDADE.get(cod_escol, -1)
    grau_tit = TRADUCAO_ESCOLARIDADE.get(cod_tit, -1)

    deno_escol = dados.get('DENO_ESCOL', '')
    deno_tit = dados.get('DENO_TIT', '')

    # Lógica de comparação
    if grau_escol >= 0 and grau_tit >= 0:
        return deno_escol if grau_escol >= grau_tit else deno_tit
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
arquivo_insc = 'Pescad_InscUFMG.txt'
mapa_insc = carregar_dicionario_inscricoes(diretorio,arquivo_insc)
caminho_completo = os.path.join(diretorio, arquivo)

# --- PROCESSAMENTO ---
dados_0 = extrair_tipo_0(diretorio, arquivo)

servidores_pessoais = extrair_tipo_1(caminho_completo, dados_0,mapa_insc) 
salvar_em_csv(servidores_pessoais, os.path.join(diretorio, 'servidores_tipo1_pessoal.csv')) 

servidores_funcionais = extrair_tipo_2(caminho_completo, dados_0,)
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