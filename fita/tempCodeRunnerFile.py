    df_funcional['CodCargo'] = df_funcional.apply(
        lambda linha:
            mapa_cad_apf_cargo.get(
                str(linha['SIAPE']).zfill(7),
                str(linha['CodCargo']).replace('.0', '')[-3:].zfill(3)
            )
            if str(linha['CodSituacao']).strip() == '19'
            else str(linha['CodCargo']).replace('.0', '')[-3:].zfill(3),
        axis=1
    )

    chave_cargo = df_funcional['GrCargo'] + df_funcional['CodCargo']

    df_funcional['DenoCargo'] = chave_cargo.apply(
        lambda codigo: mapa_deno_cargo.get(codigo, '')
    )

    df_funcional['Categoria'] = df_funcional['GrCargo'].apply(
        lambda gr_cargo: 'Docente'
        if str(gr_cargo).strip().zfill(3) in ('060', '702', '705', '706', '707')
        else 'Tec-Administrativo'
    )