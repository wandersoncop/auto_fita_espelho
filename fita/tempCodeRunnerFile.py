    lambda linha:
            linha['NOVFUNCUNORG']
            if str(linha.get('NOVFUNCSIGLA', '')).strip() != ''
            else linha['FUNCUNORG'],
        axis=1
    )