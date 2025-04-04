USE [FINANCEIRO]
GO

/****** Object:  Trigger [dbo].[TGR_APLICACAO_FINANC]    Script Date: 28/01/2025 11:48:54 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE TRIGGER [dbo].[TGR_APLICACAO_FINANC]
ON [dbo].[TB_REG_FINANC]
AFTER INSERT
AS
BEGIN
    DECLARE
        @ID_REG INT,
        @DATA_REG DATE,
        @DESC_REG VARCHAR(100),
        @LOCAL_REG VARCHAR(100),
        @VALOR_REG DECIMAL(12,2),
        @SALDO_AT DECIMAL(12,2),
        @AGREGADOR DECIMAL(12,2),
        @CATEGORIA INT;

    SELECT @CATEGORIA = IDCATEGORIA FROM INSERTED;
    
    IF @CATEGORIA = 800
    BEGIN
        SELECT 
            @ID_REG = ID_REGISTRO,
            @DATA_REG = DATA_GASTO,
            @DESC_REG = DESCRICAO,
            @LOCAL_REG = LOCAL_GASTO,
            @VALOR_REG = VALOR
        FROM INSERTED;

        SET @SALDO_AT = (SELECT TOP 1 SALDO_ATUAL FROM TB_APLICACAO_FINANC ORDER BY ID_APLICACAO DESC);
        SET @AGREGADOR = @SALDO_AT + @VALOR_REG;

        INSERT INTO TB_APLICACAO_FINANC (IDREGISTRO, DATA_APLICACAO, DESCRICAO, LOCAL_APLICACAO, VALOR_APLICACAO, SALDO_ATUAL)
        VALUES (@ID_REG, @DATA_REG, @DESC_REG, @LOCAL_REG, @VALOR_REG, @AGREGADOR);
    END
END;
GO

ALTER TABLE [dbo].[TB_REG_FINANC] ENABLE TRIGGER [TGR_APLICACAO_FINANC]
GO


