"""
script principal para processamento da Fita Espelho.

Este script organiza a execução em duas etapas:
1. Atualiza as tabelas auxiliares no banco de dados (MySQL).
2. Processa a Fita Espelho, realizando as operações necessárias.

Além disso:
- Exibe mensagens estilizadas no terminal para melhor visualização.
- Calcula e mostra o tempo total de processamento.
- Informa se o processo foi concluído com sucesso ou erro.
"""



import time
from datetime import datetime
from funcoes import (localizar_arquivo_fita)


from terminal import (
    ok, aviso, erro, linha, separador, LARGURA, tempo_operacao
)


# ==========================================================
# INÍCIO DA CONTAGEM DO TEMPO
# ==========================================================

inicio = time.time()

# ==========================================================
# CABEÇALHO
# ==========================================================

print('\n' * 2)
linha()
print("AUTO FITA ESPELHO". center(LARGURA))
print('Versão 1.0.0'. center(LARGURA))
linha()

data_hora = datetime.now().strftime('%d/%m/%y %H:%M:%S')

print(f"{'Sistema':<18}: Processamento da Fita Espelho")
print(f"{'Banco de Dados':<18}: MySQL")
print(f"{'Processamento':<18}: {data_hora}")

linha()
print()

# ==========================================================
# VERIFICA SE EXISTE O ARQUIVO DA FITA
# ==========================================================

caminho_arquivo, arquivo_encontrado, diretorio = localizar_arquivo_fita()

if caminho_arquivo is None:
    erro("Arquivo da Fita Espelho não encontrado.")
    print()
    aviso("Copie o arquivo fita_servidor_AAAA_MM.txt para a pasta Entrada.")
    print()
    linha()
    input("Pressione ENTER para sair...")
    raise SystemExit

ok(f"Arquivo encontrado: {arquivo_encontrado}")


# Somente importa os módulos do banco após encontrar a fita
from atualizar_tabelas_bd import main as atualizar_tabelas
from main import main as processar_fita
linha()
print()
aviso("ATUALIZANDO TABELAS AUXILIARES")
atualizar_tabelas()
print()
ok("Tabelas auxiliares atualizadas com sucesso.")
separador()

# ==========================================================
# ETAPA 2
# ==========================================================

print()
aviso("PROCESSANDO FITA ESPELHO")
print()


sucesso = processar_fita()
separador()

# ==========================================================
# TEMPO DE PROCESSAMENTO
# ==========================================================

fim = time.time()
tempo = fim - inicio

minutos = int(tempo // 60)
segundos = int(tempo % 60)


# ==========================================================
# RESUMO FINAL
# ==========================================================

print()
linha()

if sucesso:
    print("PROCESSO FINALIZADO COM SUCESSO")
else:
    erro('Processo interrompido. Faça os devidos ajustes antes de processar novamente.')
linha()

print()
print(' TEMPO PROCESSAMENTO')


if minutos == 0:
    tempo = f'{segundos} segundos'
else:
    tempo = f'{minutos} min {segundos} s'

tempo_operacao(f"{'Tempo total':.<30} {tempo}")
print()
linha()
print()
input("Pressione ENTER para sair...")
