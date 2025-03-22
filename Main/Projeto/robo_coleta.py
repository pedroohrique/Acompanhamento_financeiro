from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from database import database_connection
from datetime import datetime
from tkinter import messagebox
from querys import query_mensagens_coletadas
import logging
import pyautogui as tempo_carregamento

class robo_coleta_dados:
    def __init__(self):
        self.service = Service(r"C:\Windows\System32\chromedriver-win64\chromedriver.exe")
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = r"C:\Program Files\chrome-win64\chrome.exe"
        self.options.add_argument(r"user-data-dir=C:\whatappcache")
        self.options.add_argument("--profile-directory=Default")
        #self.options.add_argument("--headless")
        #self.options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.processa_mensagens()
        
    def configura_log(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(
            r"C:\Users\Pedro Henrique\Documents\Acompanhamento_financeiro\Main\Projeto\logs\log_aplicacao.txt"
        )
        file_handler.setLevel(logging.DEBUG) 
        formatter = logging.Formatter('%(asctime)s / %(levelname)s / %(name)s / %(funcName)s / %(message)s / line: %(lineno)d')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger
            
    def verifica_ultima_coleta(self):
        connection, cursor = database_connection()           
        try:
            
            query = "SELECT TOP 1 ID_COLETA FROM TB_MENSAGENS_COLETADAS ORDER BY ID_COLETA DESC"
            cursor.execute(query)
            retono_query = cursor.fetchone()
            
        except (ValueError, TypeError) as e:
            messagebox.showerror("Erro ao verificar a última coleta, verifique o arquivo de LOG")   
            log = self.configura_log("robo_coleta.py")
            log.error(f"Erro ao verificar a última mensagem: {e}")
        
        connection.commit()
        connection.close()
        return retono_query[0] if retono_query else 0
        
    def obtem_dados_web(self):
        try:
            self.driver.get("https://web.whatsapp.com")
            self.driver.implicitly_wait(10)
            elemento_caixa_busca = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p.selectable-text.copyable-text')))    
            tempo_carregamento.sleep(1.5)
            elemento_caixa_busca.send_keys("Financeiro")
            elemeno_icone_grupo = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.matched-text")))
            tempo_carregamento.sleep(1.5)
            elemeno_icone_grupo.click()
            elemento_chat = WebDriverWait(self.driver, 35).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='x1vjfegm x1cqoux5 x14yy4lh']")))
            tempo_carregamento.sleep(4)
            mensagens = elemento_chat.find_elements(By.CSS_SELECTOR, "div[class*='_akbu']")
            lista_mensagens = [row.text.split('\n') for row in mensagens]
            return lista_mensagens
            
        except Exception as e:
            messagebox.showerror("ERROR", "Erro ao coletar dados da Web, verifique o arquivo de LOG.")
            log = self.configura_log("robo_coleta.py")
            log.error(f"Erro ao localizar o elemento: {e}")
        finally:
            self.driver.quit()
            

    def processa_mensagens(self):        
        def registra_mensagens(mensagens):
            id_mensagens_pendentes = [mensagem['ID mensagem'] for mensagem in mensagens if int(mensagem['ID mensagem']) > self.verifica_ultima_coleta()]
            
            if len(id_mensagens_pendentes) > 0:                
                try:
                    for mensagem_coletada in mensagens:
                        query_mensagens_coletadas(mensagem_coletada)
                except Exception as e:
                    messagebox.showerror("Erro", "Erro ao registrar as mensagens, verifique o arquivo de LOG")
                    log = self.configura_log("robo_coleta.py")
                    log.error(f"Erro ao registrar a mensagem! ID: '{mensagem_coletada['ID mensagem']}' - ERRO: {e}")
            else:
                messagebox.showinfo("Atenção", "Não há mensagens a serem processadas!")
                log = self.configura_log("robo_coleta.py")
                log.info(f"Não há mensagens a serem processadas - Última mensagem ID: {self.verifica_ultima_coleta()}")
                
        
        lista_mensagens_processadas = []
        lista_mensagens = self.obtem_dados_web()
        
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
                        'OUTROS': 1100}
        forma_pagamento_map = {
                        'CARTÃO DE CRÉDITO': 100,
                        'CARTÃO DE DÉBITO': 200,
                        'DINHEIRO': 300,
                        'PIX': 400,
                        'SALDO DA CONTA': 500} 
        
        
        try:
            for sublista in lista_mensagens:            
                if len(sublista) == 9 and int(sublista[0]) > self.verifica_ultima_coleta():
                    dados = {
                        'ID mensagem': int(sublista[0].strip()),
                        'Data compra': str(datetime.strptime(sublista[1].strip(), "%d/%m/%Y").strftime("%Y-%m-%d")),
                        'Valor': float(sublista[2].strip()),
                        'Desc': str(sublista[3].strip()),
                        'Local': str(sublista[4].strip()),
                        'Forma': forma_pagamento_map.get(sublista[5].strip().upper()),
                        'Parcelamento': str(sublista[6].strip().upper()),
                        'QTD': int(sublista[7].strip()),
                        'Categoria': categoria_map.get(sublista[8].strip().upper())  
                    }
                    lista_mensagens_processadas.append(dados)
            registra_mensagens(mensagens=lista_mensagens_processadas)        
        except Exception as e:
            messagebox.showerror("Erro ao processar mensagens, verifique o arquivo de LOG.")
            log = self.configura_log("robo_coleta.py")
            log.error(f"Falha ao processar as mensagens recebidas: {e}")
                   
if __name__ == "__main__":
    app = robo_coleta_dados()
