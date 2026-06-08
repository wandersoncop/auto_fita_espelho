gLotacao'].apply(
        lambda codigo:mapa_unidade.get(codigo,{}).get('DenoSetor','')
    )