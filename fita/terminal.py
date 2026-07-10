#MEU!!!!!!
from colorama import init,Fore,Style
init(autoreset=True)



LARGURA = 80

def linha():
    """
    cria uma linha  com o simbolo de '='com a quantidade de caracteres
    que estive na constante LARGURA
    """
    print("=" * LARGURA)

def separador():
    """
    cria uma linha  com o simbolo de '-'com a quantidade de caracteres
    que estive na constante LARGURA
    """
    print("-" * LARGURA)

def ok(texto):
    print(Fore.GREEN + Style.BRIGHT + "✔ [OK] " + Style.RESET_ALL + texto)

def info(texto):
    print(Fore.CYAN + Style.BRIGHT + "ℹ [INFO] " + Style.RESET_ALL + texto)

def aviso(texto):
    print(Fore.YELLOW + Style.BRIGHT + "⚠ [AVISO] " + Style.RESET_ALL + texto)

def erro(texto):
    print(Fore.RED + Style.BRIGHT + "✖ [ERRO] " + Style.RESET_ALL + texto)

def tempo_operacao(texto):
    print(Fore.BLUE + Style.BRIGHT + "🕒 " + Style.RESET_ALL + texto)