import threading
import tkinter as tk
from tkinter import messagebox

# Suas importações originais
from envia_tbl_aux_bd import main as atualizar_tabelas
from main import main as processar_fita


def executar():
    try:
        # 1. Desativa o botão para evitar cliques duplos
        botao.config(state=tk.DISABLED, bg="#4b5563")

        # 2. Atualização das tabelas
        status.config(text="Status: Atualizando tabelas...", fg="#60a5fa")
        atualizar_tabelas()

        # 3. Processamento da fita
        status.config(text="Status: Processando fita...", fg="#60a5fa")
        processar_fita()

        # 4. Sucesso
        status.config(text="Status: Processo concluído.", fg="#34d399")
        messagebox.showinfo(
            "Auto Fita Espelho", "Processamento finalizado com sucesso!"
        )

    except Exception as e:
        # Caso ocorra qualquer erro em alguma das funções importadas
        status.config(text="Status: Erro no processamento.", fg="#f87171")
        messagebox.showerror(
            "Erro", f"Ocorreu um erro durante a execução:\n\n{str(e)}"
        )

    finally:
        # Sempre reativa o botão no final, dando tudo certo ou dando erro
        botao.config(state=tk.NORMAL, bg="#2563eb")


def iniciar_processamento():
    # Cria e inicia a thread secundária para não travar a interface
    threading.Thread(target=executar, daemon=True).start()


# --- Configuração da Interface Gráfica ---
janela = tk.Tk()
janela.title("Auto Fita Espelho")
janela.geometry("700x400")
janela.configure(bg="#1f2937")

titulo = tk.Label(
    janela,
    text="AUTO FITA ESPELHO",
    font=("Arial", 22, "bold"),
    fg="white",
    bg="#1f2937",
)
titulo.pack(pady=30)

subtitulo = tk.Label(
    janela,
    text="Sistema de Processamento da Fita Espelho",
    font=("Arial", 12),
    fg="#d1d5db",
    bg="#1f2937",
)
subtitulo.pack(pady=5)

botao = tk.Button(
    janela,
    text="Iniciar Processamento",
    font=("Arial", 12, "bold"),
    bg="#2563eb",
    fg="white",
    width=25,
    height=2,
    command=iniciar_processamento,
    cursor="hand2",  # Muda o ponteiro do mouse para "mãozinha" ao passar pelo botão
)
botao.pack(pady=40)

status = tk.Label(
    janela,
    text="Status: aguardando início",
    font=("Arial", 10, "italic"),
    fg="#9ca3af",
    bg="#1f2937",
)
status.pack(pady=20)

janela.mainloop()