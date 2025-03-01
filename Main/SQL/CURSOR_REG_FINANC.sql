DECLARE @ID_REGISTRO INT
DECLARE @DATA_COMPRA DATE
DECLARE @VALOR DECIMAL(18, 2)
DECLARE @QT_PARCELAS INT
DECLARE @N_PARCELA INT
DECLARE @MES_DEBITO INT
DECLARE @ANO_DEBITO INT
DECLARE @VL_PARCELA DECIMAL(18, 2)

-- Cursor para iterar sobre os registros da TB_REG_FINANC
DECLARE reg_cursor CURSOR FOR
SELECT 
    ID_REGISTRO, DATA_GASTO, VALOR, COALESCE(NULLIF(N_PARCELAS, 0), 1)
FROM TB_REG_FINANC
WHERE IDCATEGORIA NOT IN (800, 900)

-- Abrindo o cursor
OPEN reg_cursor

-- Lendo o primeiro registro
FETCH NEXT FROM reg_cursor INTO @ID_REGISTRO, @DATA_COMPRA, @VALOR, @QT_PARCELAS

-- Itera��o sobre cada registro
WHILE @@FETCH_STATUS = 0
BEGIN
    -- Inicializar o n�mero da parcela
    SET @N_PARCELA = 1

    -- Valor de cada parcela
    SET @VL_PARCELA = @VALOR / @QT_PARCELAS

    -- Loop para cada parcela
    WHILE @N_PARCELA <= @QT_PARCELAS
    BEGIN
        -- Calcula o m�s e ano da parcela
        SET @MES_DEBITO = MONTH(DATEADD(MONTH, @N_PARCELA - 1, @DATA_COMPRA))
        SET @ANO_DEBITO = YEAR(DATEADD(MONTH, @N_PARCELA - 1, @DATA_COMPRA))

        -- Insere o registro na TB_HISTORICO_FINANC
        INSERT INTO TB_HISTORICO_FINANC (IDREGISTRO, DT_GASTO, VL_TOTAL, VL_PARCELA, QT_PARCELA, N_PARCELA, MES_DEBITO_PARCELA, ANO_DEBITO_PARCELA)
        VALUES (@ID_REGISTRO, @DATA_COMPRA, @VALOR, @VL_PARCELA, @QT_PARCELAS, @N_PARCELA, @MES_DEBITO, @ANO_DEBITO)

        -- Incrementa o n�mero da parcela
        SET @N_PARCELA = @N_PARCELA + 1
    END

    -- Ler o pr�ximo registro no cursor
    FETCH NEXT FROM reg_cursor INTO @ID_REGISTRO, @DATA_COMPRA, @VALOR, @QT_PARCELAS
END

-- Fecha e desaloca o cursor
CLOSE reg_cursor
DEALLOCATE reg_cursor



