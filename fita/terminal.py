
from colorama import init,Fore,Style
init(autoreset=True)



LARGURA = 80

def linha():
    """
    Cria uma linha de '=' com a quantidade de caracteres definida em LARGURA.
    """
    print("=" * LARGURA)

def separador():
    """
    Cria uma linha de '-' com a quantidade de caracteres definida em LARGURA.
    """
    print("-" * LARGURA)

def ok(texto):
    """
    Exibe a mensagem prefixada com [OK] em verde.
    """
    print(Fore.GREEN + Style.BRIGHT + "✔ [OK] " + Style.RESET_ALL + texto)

def info(texto):
    """
    Exibe a mensagem prefixada com [INFO] em ciano.
    """
    print(Fore.CYAN + Style.BRIGHT + "ℹ [INFO] " + Style.RESET_ALL + texto)

def aviso(texto):
    """
    Exibe a mensagem prefixada com [AVISO] em amarelo.
    """
    print(Fore.YELLOW + Style.BRIGHT + "⚠ [AVISO] " + Style.RESET_ALL + texto)

def erro(texto):
    """
    Exibe a mensagem prefixada com [ERRO] em vermelho.
    """
    print(Fore.RED + Style.BRIGHT + "✖ [ERRO] " + Style.RESET_ALL + texto)

def tempo_operacao(texto):
    """
    Exibe a mensagem prefixada com [TEMPO] em azul.
    """
    print(Fore.BLUE + Style.BRIGHT + "🕒 [TEMPO] " + Style.RESET_ALL + texto)
