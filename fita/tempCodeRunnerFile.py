
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
