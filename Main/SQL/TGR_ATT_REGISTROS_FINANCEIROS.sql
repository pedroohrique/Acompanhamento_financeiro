USE [FINANCEIRO]
GO

/****** Object:  Trigger [dbo].[TGR_ATT_REGISTROS_FINANCEIROS]    Script Date: 28/01/2025 11:49:41 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[TGR_ATT_REGISTROS_FINANCEIROS]
ON [dbo].[TB_REG_FINANC]
AFTER UPDATE
AS
BEGIN
    -- Declaração de variáveis
    DECLARE
        @ID_REGISTRO INT,
        @DT_GASTO DATE,
        @V_PARCELA DECIMAL(10,2),
        @V_TOTAL DECIMAL(10,2),
        @V_PENDENTE DECIMAL(10,2),
        @QT_PARCELAS INT,
        @DT_VENCIMENTO DATE,
        @ID_FORMA INT,
        @PARCELAS_PENDENTE INT,
        @ID_CATEGORIA INT

    -- Atribuir valores da tabela INSERTED
    SELECT 
        @ID_REGISTRO = ID_REGISTRO,
        @DT_GASTO = DATA_GASTO,
        @V_TOTAL = VALOR,
        @QT_PARCELAS = N_PARCELAS,
        @ID_CATEGORIA = IDCATEGORIA,
        @ID_FORMA = IDFORMA_PAGAMENTO
    FROM INSERTED

    -- Lógica principal: Verificar a forma de pagamento
    IF @ID_FORMA != 100
    BEGIN
        -- Pagamento à vista
        SET @V_PARCELA = @V_TOTAL
        SET @DT_VENCIMENTO = @DT_GASTO
        SET @PARCELAS_PENDENTE = 0
        SET @V_PENDENTE = 0

        -- Excluir transações financeiras associadas
        DELETE FROM TB_TRANSAC_FINANC WHERE IDREGISTRO = @ID_REGISTRO
    END
    ELSE
    BEGIN
        -- Pagamento parcelado
        SET @V_PARCELA = (@V_TOTAL / @QT_PARCELAS)
        SET @DT_VENCIMENTO = DATEFROMPARTS(
                                YEAR(DATEADD(MONTH, 1, @DT_GASTO)),
                                MONTH(DATEADD(MONTH, 1, @DT_GASTO)),
                                1)
        SET @PARCELAS_PENDENTE = @QT_PARCELAS - DATEDIFF(MONTH, @DT_GASTO, GETDATE())
        SET @V_PENDENTE = @V_PARCELA * @PARCELAS_PENDENTE

        -- Verificar se já existem transações financeiras para o registro
        IF EXISTS (SELECT 1 FROM TB_TRANSAC_FINANC WHERE IDREGISTRO = @ID_REGISTRO)
        BEGIN
            -- Atualizar transação financeira
            UPDATE TB_TRANSAC_FINANC
            SET 
                IDCATEGORIA = @ID_CATEGORIA,
                DATA = @DT_GASTO,
                QTD_PARCELAS = @QT_PARCELAS,
                N_PARCELA = 1,
                VALOR_PARCELA = @V_PARCELA,
                VALOR_TOTAL = @V_TOTAL,
                DATA_VENCIMENTO_PARCELA = @DT_VENCIMENTO
            WHERE IDREGISTRO = @ID_REGISTRO
        END
        ELSE
        BEGIN
            -- Inserir nova transação financeira
            INSERT INTO TB_TRANSAC_FINANC 
                (IDREGISTRO, IDCATEGORIA, DATA, QTD_PARCELAS, N_PARCELA, VALOR_PARCELA, VALOR_TOTAL, DATA_VENCIMENTO_PARCELA)
            VALUES 
                (@ID_REGISTRO, @ID_CATEGORIA, @DT_GASTO, @QT_PARCELAS, 1, @V_PARCELA, @V_TOTAL, @DT_VENCIMENTO)
        END
    END

    -- Atualizar acompanhamento financeiro (comum para ambos os casos)
    UPDATE TB_ACOMPANHAMENTO_FINANC
    SET
        DT_COMPRA = @DT_GASTO,
        DT_PAGAMENTO = @DT_VENCIMENTO,
        VALOR_TOTAL = @V_TOTAL,
        VALOR_PARCELA = @V_PARCELA,
        VALOR_PENDENTE = @V_PENDENTE,
        QT_PARCELAS = @QT_PARCELAS,
        QT_PARCELAS_PENDENTES = @PARCELAS_PENDENTE,
        IDCATEGORIA = @ID_CATEGORIA
    WHERE IDREGISTRO = @ID_REGISTRO
END
GO

ALTER TABLE [dbo].[TB_REG_FINANC] ENABLE TRIGGER [TGR_ATT_REGISTROS_FINANCEIROS]
GO


