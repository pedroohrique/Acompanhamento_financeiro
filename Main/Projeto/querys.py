from database import database_connection
from tkinter import messagebox
from database import database_connection  
from datetime import datetime
from decimal import Decimal
from dateutil.relativedelta import relativedelta

def query_obtem_categorias() -> dict:
    try:
        connection, cursor = database_connection()
        query = "SELECT ID_CATEGORIA, DESCRICAO FROM TB_CATEGORIA"
        cursor.execute(query)
        retorno_query = cursor.fetchall()
        
        categorias = {linha[1]:linha[0] for linha in retorno_query}
        
        cursor.close()
        connection.commit()
        connection.close()
        
        return categorias
        
    except Exception as e:
        print("Erro", f"Ocorreu um erro: {e}")

def query_obtem_forma_pagamento() -> dict:
    try:
        connection, cursor = database_connection()
        query = "SELECT ID_FORMA, DESCRICAO FROM TB_FORMA_PAGAMENTO"
        cursor.execute(query)
        retorno_query = cursor.fetchall()
        
        formas = {linha[1]:linha[0] for linha in retorno_query}
        
        cursor.close()
        connection.commit()
        connection.close()
        
        return formas
        
    except Exception as e:
        print("Erro", f"Ocorreu um erro: {e}")
        
def query_altera_itens_treeview(array_dados):
    try:
        connection, cursor = database_connection()
        query = """UPDATE TB_REG_FINANC 
                SET 
                    DATA_GASTO= ?,
                    VALOR = ?,
                    DESCRICAO = ?,
                    IDCATEGORIA = ?,
                    IDFORMA_PAGAMENTO = ?,
                    PARCELAMENTO = ?,
                    N_PARCELAS = ?
                WHERE ID_REGISTRO = ?
                """
        cursor.execute(query, array_dados,)
        cursor.close()
        connection.commit()
        connection.close()
        messagebox.showinfo("Atenção!", f"Registro {array_dados[7]} alterado com sucesso")
    except Exception as e:
        messagebox.showerror("Error", f"Erro ao alterar o registro {e}")
        
def query_deleta_item_treeview(id_registro):
    query = "DELETE FROM TB_REG_FINANC WHERE ID_REGISTRO = ?"
    
    try:
        connection, cursor = database_connection()
        cursor.execute(query, id_registro)
        cursor.close()
        connection.commit()
        connection.close()
        messagebox.showinfo("Atenção", f"Registro {id_registro} excluído com sucesso!")
    except Exception as e:
        print("Erro", f"Ocorreu um erro: {e}")
        
def obtem_valores(tipo_query) -> Decimal:
        dict_query = {
            "CARTAO": """SELECT 
                            CAST(SUM(TAF.VALOR_TOTAL / COALESCE(NULLIF(TAF.QT_PARCELAS,0),1)) AS DECIMAL(10, 2)) 
                        FROM 
                            TB_ACOMPANHAMENTO_FINANC TAF 
                            JOIN TB_REG_FINANC TRF 
                            ON TAF.IDREGISTRO = TRF.ID_REGISTRO 
                        WHERE 
                            MONTH(TAF.DT_PAGAMENTO) >= ? 
                            AND YEAR(DT_PAGAMENTO) = ? 
                            AND TAF.IDCATEGORIA NOT IN (800,900) 
                            AND TRF.IDFORMA_PAGAMENTO = 100""",
            "OUTROS": """SELECT 
                            CAST(SUM(TAF.VALOR_TOTAL / COALESCE(NULLIF(TAF.QT_PARCELAS,0),1)) AS DECIMAL(10, 2)) 
                        FROM 
                            TB_ACOMPANHAMENTO_FINANC TAF 
                            JOIN TB_REG_FINANC TRF 
                            ON TAF.IDREGISTRO = TRF.ID_REGISTRO 
                        WHERE 
                            MONTH(TAF.DT_PAGAMENTO) >= ? 
                            AND YEAR(DT_PAGAMENTO) = ?
                            AND TAF.IDCATEGORIA NOT IN (800,900) 
                            AND TRF.IDFORMA_PAGAMENTO != 100""",
                            
            "TOTAL":"""SELECT 
                            CAST(SUM(TAF.VALOR_TOTAL / COALESCE(NULLIF(TAF.QT_PARCELAS,0),1)) AS DECIMAL(10, 2)) 
                        FROM 
                            TB_ACOMPANHAMENTO_FINANC TAF 
                            JOIN TB_REG_FINANC TRF 
                            ON TAF.IDREGISTRO = TRF.ID_REGISTRO 
                        WHERE 
                            MONTH(TAF.DT_PAGAMENTO) >= ? 
                            AND YEAR(DT_PAGAMENTO) = ? 
                            AND TAF.IDCATEGORIA NOT IN (800,900)"""}       
        try:
            connection, cursor = database_connection()
            mes_atual = datetime.today().month
            ano_atual = datetime.today().year
            query = dict_query.get(tipo_query.upper())
            
            cursor.execute(query, (mes_atual, ano_atual))
            valor_query = cursor.fetchone()
            cursor.close()
            connection.commit()
            connection.close()
            return valor_query[0] if valor_query and valor_query[0] is not None else 0.0
            
        except Exception as e:
            print(f"Erro ao obter os valores requisitados: {e}")
            return 0.0
        
        
def gasto_por_categoria():
        """Obtém o gasto total por categoria."""
        mes_atual = datetime.today().month
        mes_posterior = (datetime.today() + relativedelta(months=1)).month
        registro_gastos_categoria = {}
        categorias_map = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100]

        try:
            # Estabelecendo conexão explicitamente
            connection, cursor = database_connection()

            for id_categoria in categorias_map:
                query = """
                    SELECT
                        FORMAT(SUM(VALOR_PARCELA), 'N2', 'pt-BR')
                    FROM 
                        TB_ACOMPANHAMENTO_FINANC
                    WHERE 
                        IDCATEGORIA = ?
                        AND MONTH(DT_PAGAMENTO) IN (?, ?)
                    GROUP BY
                        IDCATEGORIA
                """
                cursor.execute(query, (id_categoria, mes_atual, mes_posterior))
                retorno_query = cursor.fetchone()

                registro_gastos_categoria[id_categoria] = retorno_query[0] if retorno_query and retorno_query[0] is not None else Decimal(0)

            # Fechar conexão corretamente
            connection.commit()
            cursor.close()
            connection.close()

            return registro_gastos_categoria
        except Exception as e:
            print(f"Erro ao obter gastos por categoria: {e}")
            return None
        
def obtem_aplicacao_financ() -> Decimal:
        try:
            connection, cursor = database_connection()
            query = """
               SELECT TOP 1 
               FORMAT(SALDO_ATUAL, 'N2', 'pt-BR')
               FROM TB_APLICACAO_FINANC
               ORDER BY ID_APLICACAO DESC
            """
            cursor.execute(query)
            retorno_query = cursor.fetchone()
            connection.commit()
            cursor.close()
            connection.close()
            return retorno_query[0] if retorno_query and retorno_query[0] is not None else 0.0
           
        except Exception as e:
            print(f"Erro ao obter os valores aplicados")
            return Decimal(0)
        
def dados_grafico_aplicacaoFinanc() -> dict:
        meses = []
        valores = []
        connection, cursor = database_connection()
        query = """
            SELECT
            CASE
                WHEN MONTH(DATA_APLICACAO) = 1 THEN 'JAN'
                WHEN MONTH(DATA_APLICACAO) = 2 THEN 'FEV'
                WHEN MONTH(DATA_APLICACAO) = 3 THEN 'MAR'
                WHEN MONTH(DATA_APLICACAO) = 4 THEN 'ABR'
                WHEN MONTH(DATA_APLICACAO) = 5 THEN 'MAI'
                WHEN MONTH(DATA_APLICACAO) = 6 THEN 'JUN'
                WHEN MONTH(DATA_APLICACAO) = 7 THEN 'JUL'
                WHEN MONTH(DATA_APLICACAO) = 8 THEN 'AGO'
                WHEN MONTH(DATA_APLICACAO) = 9 THEN 'SET'
                WHEN MONTH(DATA_APLICACAO) = 10 THEN 'OUT'
                WHEN MONTH(DATA_APLICACAO) = 11 THEN 'NOV'
                ELSE 'DEZ'
            END AS "MÊS",
            VALOR_APLICACAO AS "Valor"
        FROM
            TB_APLICACAO_FINANC
        WHERE 
            DATA_APLICACAO >= DATEADD(MONTH, -6, GETDATE())
        ORDER BY
            CASE 
                WHEN YEAR(DATA_APLICACAO) = ? AND MONTH(DATA_APLICACAO) = 1 THEN 2
                ELSE 2 -- Prioriza os outros meses
            END,
            YEAR(DATA_APLICACAO) ASC,
            MONTH(DATA_APLICACAO) ASC;
        """
        cursor.execute(query, datetime.today().year)
        resultado = cursor.fetchall()
        
        connection.commit()
        cursor.close()
        connection.close()
        
        for tupla in resultado:
            meses.append(tupla[0])
            valores.append(float(tupla[1]))    
        
        dados = {"Mês":meses,
                 "Valores":valores}
        
        return dados
     
def dados_grafico_gastoMensal() -> dict:
    try:
        meses = []
        valores = []
        connection, cursor = database_connection()
        query = """
            SELECT
                CASE 
                    WHEN MES_DEBITO_PARCELA = 1 THEN 'Janeiro'
                    WHEN MES_DEBITO_PARCELA = 2 THEN 'Fevereiro'
                    WHEN MES_DEBITO_PARCELA = 3 THEN 'Março'
                    WHEN MES_DEBITO_PARCELA = 4 THEN 'Abril'
                    WHEN MES_DEBITO_PARCELA = 5 THEN 'Maio'
                    WHEN MES_DEBITO_PARCELA = 6 THEN 'Junho'
                    WHEN MES_DEBITO_PARCELA = 7 THEN 'Julho'
                    WHEN MES_DEBITO_PARCELA = 8 THEN 'Agosto'
                    WHEN MES_DEBITO_PARCELA = 9 THEN 'Setembro'
                    WHEN MES_DEBITO_PARCELA = 10 THEN 'Outubro'
                    WHEN MES_DEBITO_PARCELA = 11 THEN 'Novembro'
                    ELSE 'Dezembro'
                END AS 'MÊS',
                SUM(VL_PARCELA) AS "Valor Gasto"
            FROM 
                TB_HISTORICO_FINANC
            WHERE 
                --  Converte ANO/MÊS em uma data válida
                    DATEFROMPARTS(ANO_DEBITO_PARCELA, MES_DEBITO_PARCELA, 1) BETWEEN 
                    DATEADD(MONTH, -6, CAST(GETDATE() AS DATE)) -- 6 meses atrás
                    AND EOMONTH(GETDATE()) -- Fim do mês atual
            GROUP BY
                MES_DEBITO_PARCELA,
                ANO_DEBITO_PARCELA;
        """
        cursor.execute(query)
        resultado_query = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        
        for tupla in resultado_query:
            meses.append(tupla[0])
            valores.append(float(tupla[1]))
        
        dados = {
            "Mês":meses,
            "Valores":valores
        }
        return dados
    except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
