import tkinter as tk
from tkinter import Menu, Toplevel
from tkinter import ttk, messagebox
from database import database_connection
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class checklist:
    def __init__(self, root):
        self.root = root        
        
        
    def setup_treeview(self):  
        self.interface_checklist = Toplevel(self.root)
        self.interface_checklist.title("Checklist Mensal - 2024")      
        menu_cadastro_despesa = Menu(self.interface_checklist)
        self.interface_checklist.configure(menu=menu_cadastro_despesa)
        menu_cadastro_despesa.add_command(label="Cadastrar Despesa", command=self.setup_cadastro_despesa)
        style = ttk.Style(self.interface_checklist)
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), bg="#D3D3D3", bd=2, relief="solid")
        style.configure("Treeview", font=("Arial", 11), background="#D3D3D3", fieldbackground="#D3D3D3", foreground="black", bd=2, relief="solid")
        
        columns = ["DESPESA", "VALOR_DESPESA", "DT_VENCIMENTO", "DT_PAGAMENTO", "TIPO_DESPESA", "CONTADOR_DESPESA"]
        headings = ["Despesa", "Valor R$", "Data Vencimento", "Data Pagamento", "Tipo Despesa", "N Pagamento"]
        widths = [120, 120, 150, 150, 120, 120]
        
        self.treeview_checklist = ttk.Treeview(self.interface_checklist,
                                              style="Treeview",
                                              columns=columns,
                                              show="headings",
                                              height=15)
        self.treeview_checklist.pack(fill="both", expand=True, padx=10, pady=10)
        
        for col, heading, width in zip(columns, headings, widths):
            self.treeview_checklist.heading(col, text=heading, anchor="center")
            self.treeview_checklist.column(col, width=width, anchor="center")
            
        self.lista_dados_Treeview_Checklist()
        self.treeview_checklist.bind("<Double-1>", self.dialogo_alterar_excluir)
        
               
    def setup_cadastro_despesa(self):
        interface_cadastro_despesa = Toplevel(self.interface_checklist)
        interface_cadastro_despesa.title("Cadastro de Despesas")
        largura_interface, altura_interface = 370, 200
        tp_despesas = ["Recorrente", "Não recorrente"]
        interface_cadastro_despesa.geometry(f"{largura_interface}x{altura_interface}")
        
        #Instanciamento dos labels
        label_despesa = tk.Label(interface_cadastro_despesa,
                                 text="Despesa",
                                 font=("Arial", 12, "bold"))
        label_valor_despesa = tk.Label(interface_cadastro_despesa,
                                       text="Valor despesa:",
                                       font=("Arial", 12, "bold"))
        label_dt_vencimento = tk.Label(interface_cadastro_despesa,
                                       text="Data Vencimento:",
                                       font=("Arial", 12, "bold"))
        label_tp_despesa = tk.Label(interface_cadastro_despesa,
                                    text="Tipo despesa:",
                                    font=("Arial", 12, "bold"))
        
        #Posicionamento dos Labels
        label_despesa.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        label_valor_despesa.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        label_dt_vencimento.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        label_tp_despesa.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        #Instanciamento dos Entrys 
        self.entry_despesa = tk.Entry(interface_cadastro_despesa,
                                      font=("Arial", 12))
        self.entry_valor_despesa = tk.Entry(interface_cadastro_despesa,
                                            font=("Arial", 12))
        self.entry_dt_vencimento = tk.Entry(interface_cadastro_despesa,
                                            font=("Arial", 12))
        self.combobox_tp_despesa = ttk.Combobox(interface_cadastro_despesa,
                                                values=tp_despesas,
                                                font=("Arial", 12))
        
        #Posicionamento dos Entrys
        self.entry_despesa.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.entry_valor_despesa.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.entry_dt_vencimento.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.combobox_tp_despesa.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        cadastrar_despesa = tk.Button(interface_cadastro_despesa, text="Cadastrar", command=self.cadastra_despesa, borderwidth=5, font=("Arial", 15, "bold"), bg="#4CAF50", fg="#FFFFFF", relief="raised", bd=1)
        cadastrar_despesa.grid(row=4, column=0, columnspan=2, padx=10, pady=15, sticky="NSEW")
           
    def cadastra_despesa(self):
        try:
            connection, cursor = database_connection()
            if all([self.entry_despesa.get().strip(), 
                    self.entry_dt_vencimento.get().strip(), 
                    self.entry_valor_despesa.get().strip(), 
                    self.combobox_tp_despesa.get(), 
                    connection, 
                    cursor]):
                
                valor_to_float = float(self.entry_valor_despesa.get())
                num_pagamento = 1
                dt_pagamento = None
                dt_registro = date.today()
                data_convertida = datetime.strptime(self.entry_dt_vencimento.get(), "%d-%m-%Y").strftime("%Y-%m-%d")
                cursor.execute('INSERT INTO TB_CHECKLIST_FINANC (DESPESA, VALOR_DESPESA, DT_REGISTRO, DT_VENCIMENTO, DT_PAGAMENTO, TIPO_DESPESA, CONTADOR_PAGAMENTO) VALUES  (?, ?, ?, ?, ?, ?, ?)', 
                               (self.entry_despesa.get(), 
                                valor_to_float,
                                dt_registro, 
                                data_convertida, 
                                dt_pagamento, 
                                self.combobox_tp_despesa.get(), 
                                num_pagamento))
                connection.commit()
        except(ValueError, TypeError) as error:
            messagebox.showerror("Erro", f"Ocorreu um erro: {error}")
        finally:
            cursor.close() 
            connection.close()     
        self.lista_dados_Treeview_Checklist()   
    
    def lista_dados_Treeview_Checklist(self):
        for index in self.treeview_checklist.get_children():
            self.treeview_checklist.delete(index)
            
        try:
            connection, cursor = database_connection()
            query = """
                SELECT
					CF.DESPESA,
					CF.VALOR_DESPESA,
					CF.DT_VENCIMENTO,
					CF.DT_PAGAMENTO,
					CF.TIPO_DESPESA,
					CF.CONTADOR_PAGAMENTO,
                    CF.ID_DESPESA
                FROM 
                    TB_CHECKLIST_FINANC CF
                ORDER BY
                    CF.DT_VENCIMENTO ASC;
            """
            cursor.execute(query)
        except (ValueError, TypeError) as error:
            messagebox.showerror("Erro", f"Ocorreu um erro: {error}")
            
        retorno_query = cursor.fetchall()
        
        for item in retorno_query:
            self.treeview_checklist.insert("", 
                                          "end", 
                                          values=(item[0],
                                                  item[1],
                                                  item[2],
                                                  item[3],
                                                  item[4],
                                                  item[5],
                                                  item[6]))
        connection.commit()
        connection.close()
      
    def dialogo_alterar_excluir(self, Event):
    # Cria uma nova janela de diálogo
        interface_dialogo = tk.Toplevel(self.root)
        interface_dialogo.title("Escolha uma ação")
        interface_dialogo.geometry("300x150")
        interface_dialogo.resizable(False, False)
        
        # Texto da mensagem
        mensagem = tk.Label(interface_dialogo, text="O que você deseja fazer com o registro?", font=("Arial", 12))
        mensagem.pack(pady=20)

        # Botão para Alterar
        btn_alterar = tk.Button(interface_dialogo, text="Alterar", command=self.alterar_item, font=("Arial", 12, "bold"),
                                bg="#4CAF50", fg="white", width=10)
        btn_alterar.pack(side="left", padx=20)

        # Botão para Excluir
        btn_excluir = tk.Button(interface_dialogo, text="Excluir", command=self.excluir_item, font=("Arial", 12, "bold"),
                                bg="#F44336", fg="white", width=10)
        btn_excluir.pack(side="right", padx=20)

        # Torna o diálogo modal
        interface_dialogo.transient(self.root)
        interface_dialogo.grab_set()
        self.root.wait_window(interface_dialogo)
        
        
    def alterar_item(self):
        try:
            item_selecionado = self.treeview_checklist.selection()
            valor_item_selecionado = self.treeview_checklist.item(item_selecionado)['values']
            
            id_despesa = valor_item_selecionado[6]
                
               
            mensagem = messagebox.askquestion("Selecione uma opção", f"Confirmar data de pagamento para: {date.today()}?")
            
            if mensagem == "yes":
                dt_vencimento_atual = datetime.strptime(valor_item_selecionado[2], "%Y-%m-%d").date()
                dt_pagamento = date.today()
                contador_pagamento = (valor_item_selecionado[5] + 1)                
                dt_vencimento_posterior = dt_vencimento_atual + relativedelta(month=1)  
                  
                connection, cursor = database_connection()
                cursor.execute(
                    "UPDATE TB_CHECKLIST_FINANC SET DT_VENCIMENTO = ?, DT_PAGAMENTO = ?, CONTADOR_PAGAMENTO = ? WHERE ID_DESPESA = ?",
                    (dt_vencimento_posterior, dt_pagamento, contador_pagamento, id_despesa)
                )
                
                print(f"ID: {id_despesa}, DT_VENCIMENTO_posterior: {dt_vencimento_posterior}")
                connection.commit()
                connection.close()
                
                messagebox.showinfo("Aviso", f"Despesa ID: {id_despesa} alterado com sucesso!")
                self.lista_dados_Treeview_Checklist()
                self.dialogo_alterar_excluir.destroy
            else:
                messagebox.showinfo("Aviso", f"Despesa ID: {id_despesa} não foi alterado!")
                self.dialogo_alterar_excluir.destroy
                
        except IndexError:
            messagebox.showerror("Erro", "Nenhum item foi selecionado! 123")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
           
    def excluir_item(self):
        try:
            item_selecionado = self.treeview_checklist.selection()[0]
            valor_item_selecionado = self.treeview_checklist.item(item_selecionado)["values"]
            mensagem = messagebox.askquestion("Atenção", "Deseja excluír o registro selecionado?")
            
            if mensagem == "yes":
                id_despesa = valor_item_selecionado[6]
                connection, cursor = database_connection()
                query = """DELETE FROM TB_CHECKLIST_FINANC WHERE ID_DESPESA = ?"""
                cursor.execute(query, (id_despesa,))
                connection.commit()
                connection.close()
                
                messagebox.showinfo("Aviso", f"Registro ID: '{id_despesa}' excluído com sucesso!")
                self.lista_dados_Treeview_Checklist()
                self.dialogo_alterar_excluir.destroy
            
            else:
                messagebox.showinfo("Aviso", f"Despesa ID: '{id_despesa}' não foi excluído!")
                self.dialogo_alterar_excluir.destroy
        
        except IndexError:
            messagebox.showerror("Erro", "Nenhum item foi selecionado!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
