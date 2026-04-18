import os
import csv


# FUNÇÃO PARA FORMATAR OS CAMPPOS DE DATA MAS O CAMPO TEM QUE ESTAR NA LISTA campos_que_são_data LOGO ABAIXO!!!
def formatar_data(valor):
    if valor and len(valor)==8 and valor.isdigit():
        return f'{valor[0:2]}/{valor[2:4]}/{valor[4:8]}'
    return valor



def extrair_tipo_0(fita, fita_espelho):
    caminho_arquivo = os.path.join(fita, fita_espelho)
    
    with open(caminho_arquivo, 'r', encoding='latin-1') as f:
        linha0 = f.readline()
        
        # Extração do Mês/Ano (Posição 46 a 51 no manual -> índice 45:51)
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

# Mapeamento Tipo 1 baseado na sua imagem
LAYOUT_TIPO_1 = {
    "upag": (0, 9),
    "matricula": (9, 16),
    "dv_matricula": (16, 17),
    "tipo_registro": (17, 18),
    "uf_upag": (18, 20),
    "nome_servidor": (20, 80),
    "cpf": (80, 91),
    "pis_pasep": (91, 102),
    "nome_mae": (102, 152),
    "sexo": (152, 153),
    "data_nascimento": (153, 161),
    "estado_civil": (161, 162),
    "escolaridade": (162, 164),
    "cod_titulacao": (164, 166),
    "nacionalidade": (171, 172),
    "naturalidade": (172, 174),
    "pais": (174, 177),
    "ano_chegada": (177, 181),
    "dep_ir": (181, 183),
    "dep_sf": (183, 185),
    "data_primeiro_emprego": (185, 193),
    "identificacao_origem": (193, 201),
    "logradouro": (201, 241),
    "numero_endereco": (241, 247),
    "complemento_endereco": (247, 268),
    "bairro": (268, 293),
    "municipio": (293, 323),
    "cep": (323, 331),
    "uf_endereco": (331, 333),
    "rg_numero": (333, 347),
    "rg_orgao_expeditor": (347, 352),
    "rg_data_expedicao": (352, 360),
    "rg_uf": (360, 362),
    "titulo_eleitor": (362, 375)
}

def extrair_tipo_1(caminho_arquivo, header):
    lista_dados_pessoais = []
    
    # INSIRA AQUI TODOS OS CAMPOS QUE SÃO DATA
    campos_que_são_data = [
        'data_nascimento', 
        'data_primeiro_emprego', 
        'rg_data_expedicao'
    ]
    # DICIONARIOS DE TRADUÇÃO DE CAMPOS
    TRADUCAO_ESTADO_CIVIL = {
        '1': 'SOLTEIRO(A)',
        '2': 'CASADO(A)',
        '3': 'SEPARADO(A) JUDICIALMENTE',
        '4':'DIVORCIADO',
        '5': 'VIUVO(A)',
        '6': 'UNIAO ESTAVEL',
    }

    with open(caminho_arquivo, 'r', encoding='latin-1') as f:
        for linha in f:
            # Verifica se é Registro Tipo 1 (Dados Pessoais)
            if len(linha) > 18 and linha[17] == '1':
                # Começa o registro com os dados herdados do Tipo 0
                dados = {
                    'mes_fita': header['mes_fita'],
                    # 'codigo_orgao': header['codigo_orgao']
                }
                
                # Extrai cada campo do layout
                for campo, (inicio, fim) in LAYOUT_TIPO_1.items():
                    valor = linha[inicio:fim].strip()

                    if not valor:
                        dados[campo] = None
                    elif campo in campos_que_são_data:
                        dados[campo]=formatar_data(valor)

                    # --- CRIAÇÃO DA COLUNA DE TRADUÇÃO ---
                    elif campo == 'estado_civil':
                        dados[campo]= valor
                        # cria a nova coluna   
                        dados['estado_civil_desc']=TRADUCAO_ESTADO_CIVIL.get(valor,'')
                    else:
                        dados[campo]=valor    

                    
                
                lista_dados_pessoais.append(dados)    
    return lista_dados_pessoais 

# --- EXECUÇÃO ---
diretorio = r'c:\Users\Wanderson\Desktop\auto_fita_espelho'
arquivo = 'fita_espelho.txt'
caminho_completo = os.path.join(diretorio, arquivo)

# 1. Carrega o DNA do arquivo
dados_0 = extrair_tipo_0(diretorio, arquivo)

# 2. Processa os servidores vinculando ao mês/órgão
servidores_pessoais = extrair_tipo_1(caminho_completo, dados_0) 

# --- EXIBIÇÃO DETALHADA ---
if servidores_pessoais:
    print("-" * 50)
    print(f"PROCESSAMENTO CONCLUÍDO")
    print(f"Total de servidores (Tipo 1) lidos: {len(servidores_pessoais)}")
    print("-" * 50)
    
    # Imprime todos os campos do primeiro servidor para conferência
    print("DADOS DO PRIMEIRO REGISTRO EXTRAÍDO:")
    for chave, valor in servidores_pessoais[0].items():
        print(f"{chave.ljust(25)}: {valor}")
    print("-" * 50)
else:
    print("Nenhum registro do Tipo 1 foi encontrado. Verifique se a posição 18 da linha contém o caractere '1'.")

def salvar_em_csv(lista_dados,nome_arquivo):
    if not lista_dados:
        print('Lista vazia')    
        return
    colunas = lista_dados[0].keys()
    with open(nome_arquivo,'w',newline='',encoding='latin-1') as f:
        escritor = csv.DictWriter(f,fieldnames=colunas,delimiter=';',quotechar='"',quoting=csv.QUOTE_ALL)
        # ESCREVE O CABEÇALHO(NOMES DAS COLUNAS)
        escritor.writeheader()
        # ESCREVE OS DADOS
        escritor.writerows(lista_dados)
    print(f'Arquivo salvo :{nome_arquivo}')    

#   DEFINE O NOME DO ARQUIVO DE SAIDA
caminho_csv = os.path.join(diretorio,'servidores_tipo1_extraido.csv')

# CHAMA A FUNÇÃO DE SALVAR
salvar_em_csv(servidores_pessoais,caminho_csv)