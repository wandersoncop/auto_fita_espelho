from colorama import init,Fore,Style
init(autoreset=True)



LARGURA = 80

def linha():
    print("=" * LARGURA)

def separador():
    print("-" * LARGURA)

def ok(texto):
    print(Fore.GREEN + "[OK] " + Style.RESET_ALL + texto)

def info(texto):
    print(Fore.CYAN + "[INFO] " + Style.RESET_ALL + texto)

def aviso(texto):
    print(Fore.YELLOW + "[AVISO] " + Style.RESET_ALL + texto)

def erro(texto):
    print(Fore.RED + "[ERRO] " + Style.RESET_ALL + texto)