
from envia_tbl_aux_bd import main as atualizar_tabelas
from main import main as processar_fita


print("======================================")
print(" INICIANDO AUTO FITA ESPELHO")
print("======================================")

print("\n1/2 - Atualizando tabelas auxiliares...")
atualizar_tabelas()

print("\n✅ Tabelas auxiliares atualizadas com sucesso.")


print("\n2/2 - Processando fita espelho...")
processar_fita()

print("\n✅ Processo finalizado com sucesso!")
input("\nPressione ENTER para sair...")