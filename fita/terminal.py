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
    """
    exibe o prefixo '[OK]' na cor verde antes da  menssagem de  confirmação no terminal    
    """
    print(Fore.GREEN + "[OK] " + Style.RESET_ALL + texto)

def info(texto):
    """
    exibe o prefixo '[INFO]' na cor azul antes da  menssagem de  informação no terminal    
    """
    print(Fore.CYAN + "[INFO] " + Style.RESET_ALL + texto)

def aviso(texto):
    """
    exibe o prefixo '[AVISO] ' na cor amarela antes da  menssagem de  aviso no terminal    
    """
    print(Fore.YELLOW + "[AVISO] " + Style.RESET_ALL + texto)

def erro(texto):
    """
    exibe o prefixo '[ERRO] ' na cor vermelha antes da  menssagem de erro no terminal      """

    print(Fore.RED + "[ERRO] " + Style.RESET_ALL + texto)
    