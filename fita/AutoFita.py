from envia_tbl_aux_bd import main as atualizar_tabelas
from main import main as processar_fita
import time


# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

LARGURA = 80


def linha():
    print("=" * LARGURA)


def separador():
    print("-" * LARGURA)


# ==========================================================
# INÍCIO DA CONTAGEM DO TEMPO
# ==========================================================

inicio = time.time()


# ==========================================================
# CABEÇALHO
# ==========================================================

print()
linha()
print("AUTO FITA ESPELHO".center(LARGURA))
print("Processamento da Fita".center(LARGURA))
linha()
print()


# ==========================================================
# ETAPA 1
# ==========================================================

print("[1/2] Atualizando tabelas auxiliares")
separador()

atualizar_tabelas()

print()
print("✅ Tabelas auxiliares atualizadas com sucesso.")


# ==========================================================
# ETAPA 2
# ==========================================================

print()
print("[2/2] Processando fita espelho")
separador()

processar_fita()


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
print("PROCESSO FINALIZADO COM SUCESSO".center(LARGURA))
linha()

if minutos == 0:
    print(f"Tempo de processamento: {segundos} segundos")
else:
    print(f"Tempo de processamento: {minutos} min {segundos} s")

print()

input("Pressione ENTER para sair...")