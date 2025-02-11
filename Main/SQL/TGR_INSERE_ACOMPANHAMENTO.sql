USE [FINANCEIRO]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER TRIGGER [dbo].[TGR_INSERE_ACOMPANHAMENTO]
ON [dbo].[TB_REG_FINANC]
AFTER INSERT
AS
BEGIN
    -- Cursor para percorrer todas as linhas inseridas
    DECLARE @cursor CURSOR;
    DECLARE 
        @IDREG INT, -- Armazena o ID do registro
        @DT_COMPRA DATE, -- Data da compra
        @V_TOTAL DECIMAL(10,2), -- Valor total da compra
        @V_EM_ABERTO DECIMAL(10,2), -- Valor em aberto
        @V_T_P DECIMAL(10,2), -- Valor total restante da compra
        @QTD_PARCELAS_T INT, -- Quantidade total de parcelas
        @QTD_PARCELAS_P INT, -- Quantidade de parcelas pendentes
        @ID_C INT, -- ID da categoria
        @ID_F INT, -- ID da forma de pagamento
        @DT_VENCIMENTO DATE, -- Data de vencimento
        @V_PARCELA DECIMAL(10,2), -- Valor da parcela
        @MES_DEB_PARCELA INT, -- Mês da parcela
        @ANO_DEB_PARCELA INT, -- Ano da parcela
        @N_PARCELA INT; -- Número da parcela

    -- Inicializa o cursor para todas as linhas inseridas
    SET @cursor = CURSOR FOR
    SELECT 
        ID_REGISTRO, DATA_GASTO, VALOR, N_PARCELAS, IDCATEGORIA, IDFORMA_PAGAMENTO
    FROM INSERTED;

    OPEN @cursor;
    FETCH NEXT FROM @cursor INTO @IDREG, @DT_COMPRA, @V_TOTAL, @QTD_PARCELAS_T, @ID_C, @ID_F;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Valores iniciais
        SET @DT_VENCIMENTO = @DT_COMPRA;
        SET @V_EM_ABERTO = @V_TOTAL;
        SET @V_T_P = 0.0;
        SET @QTD_PARCELAS_P = 0;
        SET @MES_DEB_PARCELA = MONTH(@DT_COMPRA);
        SET @ANO_DEB_PARCELA = YEAR(@DT_COMPRA);
        SET @N_PARCELA = 1;

        -- Pagamento à vista
        IF @ID_F != 100
        BEGIN
            INSERT INTO TB_ACOMPANHAMENTO_FINANC 
            (IDREGISTRO, DT_COMPRA, DT_PAGAMENTO, VALOR_TOTAL, VALOR_PARCELA, VALOR_PENDENTE, QT_PARCELAS, QT_PARCELAS_PENDENTES, IDCATEGORIA)
            VALUES
            (@IDREG, @DT_COMPRA, @DT_VENCIMENTO, @V_TOTAL, @V_EM_ABERTO, @V_T_P, @QTD_PARCELAS_T, @QTD_PARCELAS_P, @ID_C);

            INSERT INTO TB_HISTORICO_FINANC 
            (IDREGISTRO, DT_GASTO, VL_TOTAL, VL_PARCELA, QT_PARCELA, N_PARCELA, MES_DEBITO_PARCELA, ANO_DEBITO_PARCELA)
            VALUES
            (@IDREG, @DT_COMPRA, @V_TOTAL, @V_TOTAL, @N_PARCELA, @N_PARCELA, @MES_DEB_PARCELA, @ANO_DEB_PARCELA);
        END
        ELSE -- Pagamento parcelado
        BEGIN
            SET @DT_VENCIMENTO = DATEFROMPARTS(
                YEAR(DATEADD(MONTH, 1, @DT_COMPRA)),
                MONTH(DATEADD(MONTH, 1, @DT_COMPRA)),
                1);

            SET @QTD_PARCELAS_P = @QTD_PARCELAS_T - (DATEDIFF(MONTH, @DT_COMPRA, GETDATE()));
            SET @V_PARCELA = (@V_TOTAL / @QTD_PARCELAS_T);
            SET @V_EM_ABERTO = @V_TOTAL - ((@QTD_PARCELAS_T - @QTD_PARCELAS_P) * @V_PARCELA);

            INSERT INTO TB_ACOMPANHAMENTO_FINANC 
            (IDREGISTRO, DT_COMPRA, DT_PAGAMENTO, VALOR_TOTAL, VALOR_PARCELA, VALOR_PENDENTE, QT_PARCELAS, QT_PARCELAS_PENDENTES, IDCATEGORIA)
            VALUES
            (@IDREG, @DT_COMPRA, @DT_VENCIMENTO, @V_TOTAL, @V_PARCELA, @V_EM_ABERTO, @QTD_PARCELAS_T, @QTD_PARCELAS_P, @ID_C);

            -- Loop para inserir as parcelas
            WHILE @N_PARCELA <= @QTD_PARCELAS_T
            BEGIN
                SET @MES_DEB_PARCELA = MONTH(DATEADD(MONTH, @N_PARCELA - 1, @DT_COMPRA));
                SET @ANO_DEB_PARCELA = YEAR(DATEADD(MONTH, @N_PARCELA - 1, @DT_COMPRA));

                INSERT INTO TB_HISTORICO_FINANC 
                (IDREGISTRO, DT_GASTO, VL_TOTAL, VL_PARCELA, QT_PARCELA, N_PARCELA, MES_DEBITO_PARCELA, ANO_DEBITO_PARCELA)
                VALUES 
                (@IDREG, @DT_COMPRA, @V_TOTAL, @V_PARCELA, @QTD_PARCELAS_T, @N_PARCELA, @MES_DEB_PARCELA, @ANO_DEB_PARCELA);

                SET @N_PARCELA = @N_PARCELA + 1; -- Incremento do número da parcela
            END;
        END;

        FETCH NEXT FROM @cursor INTO @IDREG, @DT_COMPRA, @V_TOTAL, @QTD_PARCELAS_T, @ID_C, @ID_F;
    END;

    CLOSE @cursor;
    DEALLOCATE @cursor;
END;
