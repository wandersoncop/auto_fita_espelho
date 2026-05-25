SELECT * FROM fita_espelho.tbl_pessoal;

SELECT count(*) from fita_espelho.tbl_pessoal;
SELECT count(SIAPE) from fita_espelho.tbl_pessoal;

SELECT SUM(qtd) AS total_repetidos
FROM (
    SELECT COUNT(*) AS qtd
    FROM fita_espelho.tbl_pessoal
    GROUP BY SIAPE
    HAVING COUNT(*) > 1
) AS repetidos;

SELECT SUM(qtd) AS total_repetidos
FROM (
    SELECT COUNT(*) AS qtd
    FROM fita_espelho.tbl_pessoal
    GROUP BY CPF
    HAVING COUNT(*) > 1
) AS repetidos;

SELECT  SEXO,count(*)AS QTD
FROM fita_espelho.tbl_pessoal
GROUP BY SEXO;

SELECT COUNT(DISTINCT PAIS)AS QTD
FROM fita_espelho.tbl_pessoal;

SELECT 
    Escolaridade,
    COUNT(*) AS TOTAL
FROM fita_espelho.tbl_pessoal
GROUP BY Escolaridade;


