CASE 
    WHEN es.grauEscolaridade IS NOT NULL 
         AND tit.grauEscolaridade IS NOT NULL THEN
        CASE 
            WHEN CAST(es.grauEscolaridade AS SIGNED) 
                 >= CAST(tit.grauEscolaridade AS SIGNED)
                THEN es.denoEscolaridade

            ELSE tit.denoEscolaridade 
        END

        -- 2. Se houver apenas Titulação válida
        WHEN tit.grauEscolaridade IS NOT NULL THEN
            tit.denoEscolaridade

        -- 3. Se houver apenas Escolaridade válida
        WHEN es.grauEscolaridade IS NOT NULL THEN
            es.denoEscolaridade

        -- 4. Se não houver titulação válida,
        -- tenta descobrir pelo incentivo PERQUALIF
        WHEN (
            p.CodTitulacao IS NULL 
            OR p.CodTitulacao = '00' 
            OR p.CodTitulacao = ''
        ) THEN
            CASE 
                WHEN riq.PERQUALIF IN (52, 50, 35) 
                    THEN 'MESTRADO'

                WHEN riq.PERQUALIF = 75 
                    THEN 'DOUTORADO'

                WHEN riq.PERQUALIF = 30 
                    THEN 'ESPECIALIZACAO NIVEL SUPERIOR'

                ELSE es.denoEscolaridade
            END

        ELSE es.denoEscolaridade
    END AS Escolaridade,