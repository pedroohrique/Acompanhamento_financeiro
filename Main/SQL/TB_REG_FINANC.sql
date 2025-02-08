USE [FINANCEIRO]
GO

/****** Object:  Table [dbo].[TB_REG_FINANC]    Script Date: 28/01/2025 11:46:40 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[TB_REG_FINANC](
	[ID_REGISTRO] [int] IDENTITY(10,10) NOT NULL,
	[DATA_REGISTRO] [date] NULL,
	[DATA_GASTO] [date] NULL,
	[VALOR] [decimal](12, 2) NULL,
	[DESCRICAO] [varchar](100) NULL,
	[LOCAL_GASTO] [varchar](100) NULL,
	[PARCELAMENTO] [char](1) NULL,
	[N_PARCELAS] [int] NULL,
	[IDCATEGORIA] [int] NULL,
	[IDFORMA_PAGAMENTO] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_REGISTRO] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[TB_REG_FINANC]  WITH CHECK ADD  CONSTRAINT [FK_FORMA_PAGAMENTO] FOREIGN KEY([IDFORMA_PAGAMENTO])
REFERENCES [dbo].[TB_FORMA_PAGAMENTO] ([ID_FORMA])
GO

ALTER TABLE [dbo].[TB_REG_FINANC] CHECK CONSTRAINT [FK_FORMA_PAGAMENTO]
GO

ALTER TABLE [dbo].[TB_REG_FINANC]  WITH CHECK ADD  CONSTRAINT [FK_IDCATEGORIA] FOREIGN KEY([IDCATEGORIA])
REFERENCES [dbo].[TB_CATEGORIA] ([ID_CATEGORIA])
GO

ALTER TABLE [dbo].[TB_REG_FINANC] CHECK CONSTRAINT [FK_IDCATEGORIA]
GO


