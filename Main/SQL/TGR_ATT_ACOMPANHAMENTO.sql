USE [FINANCEIRO]
GO

/****** Object:  Trigger [dbo].[TGR_ATT_ACOMPANHAMENTO]    Script Date: 28/01/2025 11:49:14 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE TRIGGER [dbo].[TGR_ATT_ACOMPANHAMENTO]
ON [dbo].[TB_REG_FINANC]
AFTER INSERT
AS
BEGIN
    -- Variáveis para os registros inseridos
    DECLARE @IDCATEGORIA INT;

    -- Cursor para iterar sobre os registros inseridos
    DECLARE cur_new CURSOR FOR
        SELECT IDCATEGORIA
        FROM inserted;

    OPEN cur_new;

    FETCH NEXT FROM cur_new INTO @IDCATEGORIA;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Verificar se IDCATEGORIA é 900
        IF @IDCATEGORIA = 900
        BEGIN
            DECLARE @id INT,
                    @IDREGISTRO INT,
                    @dt_compra DATE,
                    @dt_pagamento DATE,
                    @valor_total DECIMAL(10, 2),
                    @valor_pendente DECIMAL(10, 2),
                    @qt_parcelas INT,
                    @qt_parcelas_pendentes INT;

            DECLARE cur CURSOR FOR
                SELECT ID, IDREGISTRO, DT_COMPRA, DT_PAGAMENTO, VALOR_TOTAL, VALOR_PENDENTE, QT_PARCELAS, QT_PARCELAS_PENDENTES
                FROM TB_ACOMPANHAMENTO_FINANC;

            OPEN cur;

            FETCH NEXT FROM cur INTO @id, @IDREGISTRO, @dt_compra, @dt_pagamento, @valor_total, @valor_pendente, @qt_parcelas, @qt_parcelas_pendentes;

            WHILE @@FETCH_STATUS = 0
            BEGIN
                -- Atualiza as colunas de pagamento e parcelas pendentes
                IF @qt_parcelas_pendentes > 0
                BEGIN
                    SET @qt_parcelas_pendentes = @qt_parcelas_pendentes - 1;
                    SET @valor_pendente = @valor_pendente - (@valor_total / @qt_parcelas);
                    SET @dt_pagamento = DATEADD(MONTH, 1, @dt_pagamento);

                    UPDATE TB_ACOMPANHAMENTO_FINANC
                    SET DT_PAGAMENTO = @dt_pagamento,
                        VALOR_PENDENTE = @valor_pendente,
                        QT_PARCELAS_PENDENTES = @qt_parcelas_pendentes
                    WHERE ID = @id;
                END

                -- Remove o registro se todas as parcelas foram pagas
                IF @qt_parcelas_pendentes < 1
                BEGIN
                    DELETE FROM TB_ACOMPANHAMENTO_FINANC WHERE ID = @id;
                END

                FETCH NEXT FROM cur INTO @id, @IDREGISTRO, @dt_compra, @dt_pagamento, @valor_total, @valor_pendente, @qt_parcelas, @qt_parcelas_pendentes;
            END

            CLOSE cur;
            DEALLOCATE cur;
        END

        FETCH NEXT FROM cur_new INTO @IDCATEGORIA;
    END

    CLOSE cur_new;
    DEALLOCATE cur_new;
END;
GO

ALTER TABLE [dbo].[TB_REG_FINANC] ENABLE TRIGGER [TGR_ATT_ACOMPANHAMENTO]
GO


