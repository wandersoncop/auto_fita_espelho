f_funcional.loc[
            df_funcional['NrUorgExercicio'].astype(str).str.strip() == '000000000',
            'NrUorgExercicio'
        ] = ''
