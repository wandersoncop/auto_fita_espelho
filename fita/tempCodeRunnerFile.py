

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
# ETAPA 1
# ==========================================================

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