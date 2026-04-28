import os
import csv
import pandas as pd
from mapeamentos import (
    LAYOUT_TIPO_1, 
    HEADER_TIPO_1,
    LAYOUT_TIPO_2, 
    HEADER_TIPO_2,
    CAMPOS_DATA_TIPO_1, 
    CAMPOS_DATA_TIPO_2, 
    # TRADUCAO_ESTADO_CIVIL,
    TRADUCAO_DENO_ESCOL,
    TRADUCAO_TIT_FORM,
    TRADUCAO_ESCOLARIDADE,
    TRADUCAO_PAIS,
    TRADUCAO_SIT,
    TRADUCAO_CARGO,
    
)
# import csv

# import csv
# #  formata a tabela desejada
# import csv

# import csv

# import csv



def carregar_tabela_apoio(caminho_arquivo):
    traducao = {}
    if not os.path.exists(caminho_arquivo):
        print(f"ERRO: Arquivo não encontrado em: {caminho_arquivo}")
        return traducao  # Retorna vazio se não achar o arquivo
    try:
        with open(caminho_arquivo, mode='r', encoding='latin-1') as f:
            conteudo = f.read().replace('"', '')
            linhas = conteudo.splitlines()
            
            for i, linha in enumerate(linhas):
                if not linha.strip(): continue # Pula linhas vazias
                colunas = linha.split(';')
                if len(colunas) >= 2:
                    chave = colunas[0].strip()
                    
                    # Pula cabeçalho se a primeira coluna for texto de identificação
                    if i == 0 and chave.lower() in ['chaveclasse', 'cod', 'codigo', 'id', 'chave']:
                        continue
                    
                    # Se tiver 4 colunas (Classe), pega a última. Senão, pega a segunda.
                    indice_desc = 3 if len(colunas) >= 4 else 1
                    
                    if chave:
                        traducao[chave] = colunas[indice_desc].strip()
        print(f"SUCESSO: {caminho_arquivo} carregado.")
    except FileNotFoundError:
        print(f"ERRO: Arquivo não encontrado em: {caminho_arquivo}")
    except Exception as e:
        print(f"ERRO ao carregar {caminho_arquivo}: {e}")
    return traducao


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

# carrega as traduções da tabelas
# Agora essa função serve para TUDO
# Mude estas linhas no topo do seu código:

MAPA_CLASSES = carregar_tabela_apoio(r'C:\Users\\Desktop\auto_fita_espelho\Tabela Classe.txt')

MAPA_ESTADO_CIVIL = carregar_tabela_apoio(r'C:\Users\wandersoncop\Desktop\auto_fita_espelho\Tabela Estado Civil.txt')
# MAPA_ESCOLARIDADE = carregar_tabela_apoio(r'C:\Userswandersoncop\wandersoncop\Desktop\auto_fita_espelho\Tabela Escolaridade.txt')

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
                
                # Estado Civil------------------------------------------
                codigo_eciv = str(dados.get('ECIV') or '').strip()
                dados['DENO_E_CIV'] = MAPA_ESTADO_CIVIL.get(codigo_eciv, 'NÃO INFORMADO')
                
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
                
    return lista_dados_pessoais, mapa_nomes

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



 


def extrair_tipo_2(caminho_arquivo, header, mapa_inscricoes, mapa_nomes):
    lista_dados_funcionais = []
    valor_do_mes = header.get('mes_fita') or header.get('MES_FITA')

     # 1. Extração do layout com FORMATAÇÃO DE DATA integrada
    


    
    with open(caminho_arquivo, 'r', encoding='latin-1') as f:
        for linha in f:
            # Verifica se a linha tem o tipo 2 na posição 17
            if len(linha) > 18 and linha[17] == '2':
                dados = {'mes_fita': valor_do_mes}
            # FORMATA OS CAMPO DE DATA
               # --- 1. EXTRAÇÃO ÚNICA COM FORMATAÇÃO DE DATA ---
                for campo, (inicio, fim) in LAYOUT_TIPO_2.items():
                    valor = linha[inicio:fim].strip()
                    
                    if not valor:
                        dados[campo] = ""
                    elif campo in CAMPOS_DATA_TIPO_2:
                        # Formata aqui e já salva no dicionário
                        dados[campo] = formatar_data(valor)
                    else:
                        dados[campo] = valor

                   

                # 2. CRIAÇÃO DO CAMPO CAT E IDENTIFICAÇÃO DA LETRA
                gr_cargo = dados.get('GRCARGO', '')
                cat_letra = 'M' if gr_cargo in ('060', '702', '705', '706', '707') else 'T'
                dados['CAT'] = 'Docente' if cat_letra == 'M' else 'Tec-Administrativo'

                # 3. CONCATENAÇÃO DA CHAVE E TRADUÇÃO DA CLASSE (DenoClasse)
              
                val_classe = dados.get('CLASSE') or dados.get('CLAS') or ''
                ref = dados.get('REF') or ''
                primeiro_dig_ref = ref[0] if ref else ""

                # Montagem inicial da chave (Ex: M + 6 = M6)
                chave_final = f"{cat_letra}{val_classe}"
                

                # Regra especial para o cargo 705 (Docentes específicos)
                if gr_cargo == '705' and val_classe == '4' and primeiro_dig_ref != '4':
                    chave_final = f"{cat_letra}{gr_cargo}{val_classe}{primeiro_dig_ref}"

                # Salva a chave montada para conferência
                dados['ChaveClass'] = chave_final
                
                # Realiza a tradução usando o MAPA_CLASSES carregado do CSV
                # Se não encontrar no CSV, ele mostra a chave entre parênteses para você saber o que faltou
                #dados['DenoClasse'] = MAPA_CLASSES.get(chave_final,'')
                # Isso vai te mostrar no CSV se o erro é 'Chave não encontrada' ou 'Dicionário Vazio'
                if not MAPA_CLASSES:
                    dados['DenoClasse'] = "ERRO: DICIONARIO VAZIO"
                else:
                    dados['DenoClasse'] = MAPA_CLASSES.get(chave_final, f"NAO LOCALIZADO: {chave_final}")

                # 4. CRIAÇÃO DO CODCARGO (GRCARGO + CARGO)
                v_gr = str(dados.get('GRCARGO', '')).zfill(3)
                v_ca = str(dados.get('CARGO', '')).zfill(3)
                dados['CodCargo'] = v_gr + v_ca

                # 5. CORRESPONDÊNCIA (MATRICULA, NOME E INSCRIÇÃO)
                matric_func = str(dados.get('MATRIC', '')).strip()
                dados['NOME'] = mapa_nomes.get(matric_func, 'NOME NAO ENCONTRADO')
                dados['InscUFMG'] = mapa_inscricoes.get(matric_func, '')

                # 6. TRADUÇÃO DA SITUAÇÃO E CARGO 
                cod_sit = str(dados.get('SIT') or '').zfill(2)
                dados['DENO_SIT'] = TRADUCAO_SIT.get(cod_sit, f'SIT {cod_sit}')
                
                cod_cargo_full = dados['CodCargo'].zfill(6)
                dados['DENOCARG'] = TRADUCAO_CARGO.get(cod_cargo_full, f'DENOCARG {cod_cargo_full}')

                # REGRA DO RT SE FOR '99' VIRA 'DE'
                valor_rtrab = dados.get('RTRAB','').strip() # pega o valor bruto de RTRAB
                if valor_rtrab == '99':
                    dados['RT'] = 'DE'
                else:
                    dados['RT']= valor_rtrab

                # 7. MONTAGEM FINAL PARA O CSV (Conforme a ordem do HEADER_TIPO_2)
                try:
                    dados_ordenado = {campo: dados.get(campo) for campo in HEADER_TIPO_2}
                    lista_dados_funcionais.append(dados_ordenado)
                except Exception as e:
                    print(f"Erro de mapeamento no Header: {e}")
                
    return lista_dados_funcionais

def salvar_em_csv(lista_dados, nome_arquivo):
    if not lista_dados:
        print(f'Aviso: Lista para {nome_arquivo} está vazia.')    
        return
    colunas = lista_dados[0].keys()
    with open(nome_arquivo, 'w', newline='', encoding='latin-1') as f:
        escritor = csv.DictWriter(f, fieldnames=colunas, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL,lineterminator='\n')
        escritor.writeheader()
        escritor.writerows(lista_dados)
    print(f'Arquivo salvo: {nome_arquivo}')       

# import os

# --- EXECUÇÃO ---

# Identifica automaticamente se o PC é Wanderson, Wandersoncop ou qualquer outro
diretorio = os.path.join(os.path.expanduser("~"), "Desktop", "auto_fita_espelho")

arquivo = 'fita_espelho.txt'
arquivo_insc = 'Pescad_InscUFMG.txt'
caminho_classe = os.path.join(diretorio, 'Tabela Classe.txt')
MAPA_CLASSES = carregar_tabela_apoio(caminho_classe)

# Agora o código usa o diretório dinâmico para carregar os arquivos
mapa_insc = carregar_dicionario_inscricoes(diretorio, arquivo_insc)
caminho_completo = os.path.join(diretorio, arquivo)

# Exemplo de como abrir a Tabela de Estado Civil usando o mesmo diretório
# caminho_estado_civil = os.path.join(diretorio, 'Tabela Estado Civil.txt')

print(f"Diretório detectado: {diretorio}")

# --- PROCESSAMENTO ---
dados_0 = extrair_tipo_0(diretorio, arquivo)

servidores_pessoais,mapa_nomes_aux = extrair_tipo_1(caminho_completo, dados_0,mapa_insc) 
salvar_em_csv(servidores_pessoais, os.path.join(diretorio, 'servidores_tipo1_pessoal.csv')) 

servidores_funcionais = extrair_tipo_2(caminho_completo, dados_0,mapa_insc,mapa_nomes_aux)
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