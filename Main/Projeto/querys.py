from database import database_connection
from tkinter import messagebox
from database import database_connection  
from datetime import datetime
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from logger import configura_log

def query_obtem_categorias() -> dict:
    try:
        connection, cursor = database_connection()
        query = "SELECT ID_CATEGORIA, DESCRICAO FROM TB_CATEGORIA"
        cursor.execute(query)
        retorno_query = cursor.fetchall()
        categorias = {linha[1]:linha[0] for linha in retorno_query}
        connection.commit()  
        return categorias
        
    except Exception as e:
        log = configura_log("querys.py")
        log.error(f"Erro ao executar a query: {e}")
    finally:
        cursor.close()
        connection.close()

def query_obtem_forma_pagamento() -> dict:
    try:
        connection, cursor = database_connection()
        query = "SELECT ID_FORMA, DESCRICAO FROM TB_FORMA_PAGAMENTO"
        cursor.execute(query)
        retorno_query = cursor.fetchall()
        formas = {linha[1]:linha[0] for linha in retorno_query}
        connection.commit()
        return formas
        
    except Exception as e:
        log = configura_log("querys.py")
        log.error(f"Falha ao executar a query: {e}")
    finally:
        cursor.close()
        connection.close()
        
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
        connection.commit()
        messagebox.showinfo("Atenção!", f"Registro {array_dados[7]} alterado com sucesso")
    except Exception as e:
        messagebox.showerror("Error", f"Erro ao alterar o registro: {e}")
        log = configura_log("querys.py")
        log.error(f"Erro ao alterar o registro: {e}") 
    finally:
        cursor.close()
        connection.close()
        
def query_deleta_item_treeview(id_registro):
    query = "DELETE FROM TB_REG_FINANC WHERE ID_REGISTRO = ?"
    
    try:
        connection, cursor = database_connection()
        cursor.execute(query, id_registro)
        connection.commit()
        messagebox.showinfo("Atenção", f"Registro {id_registro} excluído com sucesso!")
    except Exception as e:
        messagebox.showerror("Error", f"Falha ao excluir o item da Treeview: {e}")
        log = configura_log("querys.py")
        log.error(f"Falha ao excluir o item da Treeview: {e}")       
    finally:
        cursor.close()
        connection.close()
        
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
            connection.commit()
            return valor_query[0] if valor_query and valor_query[0] is not None else 0.0
            
        except Exception as e:
            log = configura_log("querys.py")
            log.error(f"Falha ao executar a query: {e}")       
            return 0.0
        finally:
            cursor.close()
            connection.close()
        
        
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

            connection.commit()

            return registro_gastos_categoria
        except Exception as e:
            log = configura_log("querys.py")
            log.error(f"Falha ao executar a query: {e}")       
            return 0.0
        finally:
            cursor.close()
            connection.close()
        
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
        return retorno_query[0] if retorno_query and retorno_query[0] is not None else 0.0
    except Exception as e:
        log = configura_log("querys.py")
        log.error(f"Falha ao executar a query: {e}")       
    finally:
        cursor.close()
        connection.close()
        
def dados_grafico_aplicacaoFinanc() -> dict:  
    meses = []
    valores = []
    try:
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
        
        for tupla in resultado:
            meses.append(tupla[0])
            valores.append(float(tupla[1]))    
        
        dados = {"Mês":meses,
                 "Valores":valores}
        return dados
    
    except Exception as e:
        log = configura_log("querys.py")
        log.error(f"Falha ao executar a query: {e}")       
    finally:
        cursor.close()
        connection.close()
     
def dados_grafico_gastoMensal() -> dict:
    try:
        meses = []
        valores = []
        connection, cursor = database_connection()
        query = """
            SELECT
                CASE 
                    WHEN THF.MES_DEBITO_PARCELA = 1 THEN 'Janeiro'
                    WHEN THF.MES_DEBITO_PARCELA = 2 THEN 'Fevereiro'
                    WHEN THF.MES_DEBITO_PARCELA = 3 THEN 'Março'
                    WHEN THF.MES_DEBITO_PARCELA = 4 THEN 'Abril'
                    WHEN THF.MES_DEBITO_PARCELA = 5 THEN 'Maio'
                    WHEN THF.MES_DEBITO_PARCELA = 6 THEN 'Junho'
                    WHEN THF.MES_DEBITO_PARCELA = 7 THEN 'Julho'
                    WHEN THF.MES_DEBITO_PARCELA = 8 THEN 'Agosto'
                    WHEN THF.MES_DEBITO_PARCELA = 9 THEN 'Setembro'
                    WHEN THF.MES_DEBITO_PARCELA = 10 THEN 'Outubro'
                    WHEN THF.MES_DEBITO_PARCELA = 11 THEN 'Novembro'
                    ELSE 'Dezembro'
                END AS 'MÊS',
                SUM(THF.VL_PARCELA) AS "Valor Gasto"
            FROM 
                TB_HISTORICO_FINANC THF
				JOIN TB_REG_FINANC TRF ON THF.IDREGISTRO = TRF.ID_REGISTRO
            WHERE 
                --  Converte ANO/MÊS em uma data válida
                    DATEFROMPARTS(THF.ANO_DEBITO_PARCELA, THF.MES_DEBITO_PARCELA, 1) BETWEEN 
                    DATEADD(MONTH, -6, CAST(GETDATE() AS DATE)) -- 6 meses atrás
                    AND EOMONTH(GETDATE()) -- Fim do mês atual
					AND TRF.IDCATEGORIA NOT IN (800,900)
            GROUP BY
                THF.MES_DEBITO_PARCELA,
                THF.ANO_DEBITO_PARCELA;
        """
        cursor.execute(query)
        resultado_query = cursor.fetchall()
        connection.commit()
        
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
            log = configura_log("querys.py")
            log.error(f"Falha ao executar a query: {e}")       
    finally:
        cursor.close()
        connection.close()
        
def query_mensagens_coletadas(dicionario):
    
    query_tb_mensagens_coletadas = "INSERT INTO TB_MENSAGENS_COLETADAS (ID_COLETA, DATA_COLETA, DATA_GASTO, DESCRICAO) VALUES (?, GETDATE(), ?, ?)"
    query_tb_reg_financ = "INSERT INTO TB_REG_FINANC (DATA_REGISTRO, DATA_GASTO, VALOR, DESCRICAO, LOCAL_GASTO, PARCELAMENTO, N_PARCELAS, IDCATEGORIA, IDFORMA_PAGAMENTO) VALUES (GETDATE(), ?, ?, ?, ?, ?, ?, ?, ?)"
    
    try:
        connection, cursor = database_connection()
        cursor.execute(
                query_tb_mensagens_coletadas,
                (dicionario['ID mensagem'], dicionario['Data compra'], dicionario['Desc'])
        )
        
        if cursor.rowcount > 0:
            pass
        else:
            log = configura_log("querys.py")
            log.error(f"Falha ao inserir na TB_MENSAGENS_COLETADAS, ID: {dicionario['ID mensagem']}")
                   
        cursor.execute(
            query_tb_reg_financ,
            (dicionario['Data compra'], dicionario['Valor'], dicionario['Desc'], dicionario['Local'], dicionario['Parcelamento'], dicionario['QTD'], dicionario['Categoria'],
            dicionario['Forma'])
        )
        
        if cursor.rowcount > 0:
            log = configura_log("querys.py")
            log.info(f"Mensagem coletada com sucesso! ID: {dicionario['ID mensagem']}")
        else:
            log = configura_log("querys.py")
            log.error(f"Falha ao inserir na TB_REG_FINANC, ID: {dicionario['ID mensagem']}")
         
        connection.commit()

    except Exception as e:
        messagebox.showerror("Erro", "Falha ao inserir a mensagem no banco de dados, verifique o arquivo de LOG")
        log = configura_log("querys.py")
        log.error(f"Falha ao inserir a mensagem no banco de dados: {e}")
    
    finally:
        cursor.close()
        connection.close()
