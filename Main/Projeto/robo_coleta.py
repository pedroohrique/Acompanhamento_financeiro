from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from database import database_connection
from datetime import datetime, date
from tkinter import messagebox
import pyautogui as tempo_carregamento

class robo_coleta_dados:
    def __init__(self):
        self.service = Service(r"C:\Windows\System32\chromedriver-win64\chromedriver.exe")
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = r"C:\Program Files\chrome-win64\chrome.exe"
        self.options.add_argument(r"user-data-dir=C:\whatappcache")
        self.options.add_argument("--profile-directory=Default")
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.processa_mensagens()
            
    def verifica_ultima_coleta(self):
        connection, cursor = database_connection()           
        try:
            query = "SELECT TOP 1 ID_COLETA FROM TB_MENSAGENS_COLETADAS ORDER BY ID_COLETA DESC"
            cursor.execute(query)
        except (ValueError, TypeError) as e:
            messagebox.showerror("Erro ao verificar mensagens", f"{e}")
        
        retono_query = cursor.fetchone()
        connection.commit()
        connection.close()
        return retono_query[0] if retono_query else 0
        
    def obtem_dados_web(self):
        try:
            self.driver.get("https://web.whatsapp.com")
            elemento_caixa_busca = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p.selectable-text.copyable-text')))    
            tempo_carregamento.sleep(1.5)
            elemento_caixa_busca.send_keys("Financeiro neno e nena")
            elemeno_icone_grupo = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.matched-text")))
            tempo_carregamento.sleep(1.5)
            elemeno_icone_grupo.click()
            elemento_chat = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='x1vjfegm x1cqoux5 x14yy4lh']")))
            tempo_carregamento.sleep(4)
            mensagens = elemento_chat.find_elements(By.CSS_SELECTOR, "div[class*='_akbu']")
            lista_mensagens = [row.text.split('\n') for row in mensagens]
            return lista_mensagens
            
        except Exception as e:
            print(f"Erro ao localizar o elemento: {e}")
        finally:
            self.driver.quit()
    
    
    def processa_mensagens(self):
        lista_mensagens_processadas = []
        lista_mensagens = self.obtem_dados_web()
        
        for sublista in lista_mensagens:
            id_ultima_coleta = self.verifica_ultima_coleta()
            try:
                if len(sublista) == 9:
                    dados = {
                        'ID mensagem': sublista[0],
                        'Data compra': sublista[1],
                        'Valor': sublista[2],
                        'Desc': sublista[3],
                        'Local': sublista[4],
                        'Forma': sublista[5],
                        'Parcelamento': sublista[6],
                        'QTD': sublista[7],
                        'Categoria': sublista[8]  
                    }

                    lista_mensagens_processadas.append(dados)
            except Exception as e:
                messagebox.showerror("Erro ao processar mensagens", f"{e}")
                
                
            try:
                data_reg = date.today()
                for dicionario in lista_mensagens_processadas:
                    data_compra_conv = datetime.strptime(dicionario['Data compra'].strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
                    id_mensagem = int(dicionario["ID mensagem"])
                    connection, cursor = database_connection()
                    if connection and cursor and id_mensagem > id_ultima_coleta:
                        print(f"ID ÚLTIMA COLETA: {id_ultima_coleta}, ID MENSAGEM ATUAL: {id_mensagem}")
                        categoria_map = {
                        'ALIMENTAÇÃO': 100,
                        'MORADIA': 200,
                        'TRANSPORTE': 300,
                        'SAÚDE': 400,
                        'LAZER E ENTRETERIMENTO': 500,
                        'COMPRAS': 600,
                        'GASTOS OCASIONAIS': 700,
                        'INVESTIMENTOS E APLICAÇÕES': 800,
                        'PAGAMENTO FATURA': 900,
                        'EDUCAÇÃO': 1000,
                        'OUTROS': 1100
                        }
                        forma_pagamento_map = {
                        'CARTÃO DE CRÉDITO': 100,
                        'CARTÃO DE DÉBITO': 200,
                        'DINHEIRO': 300,
                        'PIX': 400,
                        'SALDO DA CONTA': 500
                        }     
                        cursor.execute(
                            'INSERT INTO TB_MENSAGENS_COLETADAS (ID_COLETA, DATA_COLETA, DATA_GASTO, DESCRICAO) VALUES (?, ?, ?, ?)',
                            (
                            id_mensagem,
                            data_reg, 
                            data_compra_conv,                  
                            dicionario['Desc'].strip(), 
                            )
                        )                  
                        cursor.execute(
                            'INSERT INTO TB_REG_FINANC (DATA_REGISTRO, DATA_GASTO, VALOR, DESCRICAO, LOCAL_GASTO, PARCELAMENTO, N_PARCELAS, IDCATEGORIA, IDFORMA_PAGAMENTO) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            (data_reg, 
                            data_compra_conv, 
                            dicionario['Valor'].strip(), 
                            dicionario['Desc'].strip(), 
                            dicionario['Local'].strip(), 
                            dicionario['Parcelamento'].strip(),
                            dicionario['QTD'].strip(),
                            categoria_map.get(dicionario['Categoria'].strip().upper(), None),
                            forma_pagamento_map.get(dicionario['Forma'].strip().upper(), None))
                        )
                        
                    else:
                        print(f"Não há mensagens a serem coletadas! Ultima coleta realizada ID: {id_ultima_coleta}")
                
                connection.commit()
                connection.close() 
                           
            except Exception as e:
                messagebox.showerror("Erro", f"{e}")
        messagebox.showinfo("Atenção!",f"Última coleta realizada - Mensagem ID = {id_ultima_coleta}")  
        
if __name__ == "__main__":
    app = robo_coleta_dados()
