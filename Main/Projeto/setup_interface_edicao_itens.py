import tkinter as tk
from tkinter import ttk, messagebox
from querys import query_obtem_categorias, query_obtem_forma_pagamento, query_altera_itens_treeview
from datetime import datetime

class edicao_itens:

    def __init__(self,  array_dados):
        self.root = tk.Tk()
        self.root.title("Edição de Itens")
        self.root.geometry("380x375")
        self.root.resizable(False, False)
        self.array_dados = array_dados
        self.categorias = [categoria for categoria in query_obtem_categorias()]
        self.formas = [forma for forma in query_obtem_forma_pagamento()]
        self.categorias_map = query_obtem_categorias()
        self.forma_pagamento_map = query_obtem_forma_pagamento()
        self.janela_edicao()

    def valida_input_usuario(self) -> bool:
        try:
            self.entry_dt_compra .get() is not None
            self.entry_v_total.get() is not None
            self.combobox_categoria.get() is not None
            self.entry_descricao.get() is not None
            self.combobox_forma_pagamento.get() is not None
            self.combobox_parcelamento.get() is not None
            self.entry_n_parcelas.get() is not None
            return all([
                self.entry_dt_compra,
                self.entry_v_total,
                self.combobox_categoria,
                self.entry_descricao,
                self.combobox_forma_pagamento,
                self.combobox_parcelamento,
                self.entry_n_parcelas
            ])  
        except ValueError as e:
            messagebox.showerror("Erro", f"Verifique as informações inseridas: {str(e)}")
            return False
    
    def altera_item_treeview(self):
        if self.valida_input_usuario():
            id_registro = self.array_dados[7]
            dt_compra = datetime.strptime(self.entry_dt_compra.get(), '%d/%m/%Y').date()
            valor_compra = self.entry_v_total.get()[:-3].strip()
            descricao = self.entry_descricao.get()
            id_categoria = self.categorias_map.get(self.combobox_categoria.get())
            id_forma_pagamento = self.forma_pagamento_map.get(self.combobox_forma_pagamento.get())
            parcelamento = self.combobox_parcelamento.get()[0]
            n_parcelas = self.entry_n_parcelas.get()
            
            dados = (dt_compra,
                     float(valor_compra),
                     descricao,
                     int(id_categoria),
                     int(id_forma_pagamento),
                     parcelamento,
                     int(n_parcelas),
                     int(id_registro))
            
            query_altera_itens_treeview(dados)
            
    def janela_edicao(self):         
        label_dt_compra = tk.Label(self.root, text="Data Compra:", font=('Helvetica', 12, "bold"))
        label_dt_compra.grid(row=0, column=0, padx=10, pady=10, sticky="w")
                
        label_v_total = tk.Label(self.root, text="Valor Total:", font=('Helvetica', 12, "bold"))
        label_v_total.grid(row=1, column=0, padx=10, pady=10, sticky="w")
                
        label_categoria = tk.Label(self.root, text="Categoria:", font=('Helvetica', 12, "bold"))
        label_categoria.grid(row=2, column=0, padx=10, pady=10, sticky="w")
                
        label_descricao = tk.Label(self.root, text="Descrição:", font=('Helvetica', 12, "bold"))
        label_descricao.grid(row=3, column=0, padx=10, pady=10, sticky="w")
                
        label_forma_pagamento = tk.Label(self.root, text="Forma Pagamento:", font=('Helvetica', 12, "bold"))
        label_forma_pagamento.grid(row=4, column=0, padx=10, pady=10, sticky="w")
                
        label_parcelamento = tk.Label(self.root, text="Parcelamento:", font=('Helvetica', 12, "bold"))
        label_parcelamento.grid(row=5, column=0, padx=10, pady=10, sticky="w")
                
        label_n_parcelas = tk.Label(self.root, text="Qt Parcelas:", font=('Helvetica', 12, "bold"))
        label_n_parcelas.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        
        
        self.entry_dt_compra = tk.Entry(self.root, font=("Helvetica", 12))
        self.entry_dt_compra.grid(row=0, column=1, pady=10, sticky="WE")
        self.entry_dt_compra.insert(0, self.array_dados[0])
        
        self.entry_v_total = tk.Entry(self.root, font=("Helvetica", 12))
        self.entry_v_total.grid(row=1, column=1, pady=10, sticky="WE")
        self.entry_v_total.insert(0, self.array_dados[1])
        
        self.combobox_categoria = ttk.Combobox(self.root, font=("Helvetica", 12), values=self.categorias)
        self.combobox_categoria.insert(0, self.array_dados[2])
        self.combobox_categoria.grid(row=2, column=1, pady=10, sticky="WE")
        
        self.entry_descricao = tk.Entry(self.root, font=("Helvetica", 12))
        self.entry_descricao.grid(row=3, column=1, pady=10, sticky="WE")
        self.entry_descricao.insert(0, self.array_dados[3])
        
        self.combobox_forma_pagamento = ttk.Combobox(self.root, font=("Helvetica", 12), values=self.formas)
        self.combobox_forma_pagamento.insert(0, self.array_dados[4])
        self.combobox_forma_pagamento.grid(row=4, column=1, pady=10, sticky="WE")
        
        self.combobox_parcelamento = ttk.Combobox(self.root, font=("Helvetica", 12), values=["Sim", "Não"])
        self.combobox_parcelamento.grid(row=5, column=1, pady=10, sticky="WE")
        self.combobox_parcelamento.insert(0, "Sim" if self.array_dados[5] == "S" else "N")
        
        self.entry_n_parcelas = tk.Entry(self.root, font=("Helvetica", 12))
        self.entry_n_parcelas.grid(row=6, column=1, pady=10, sticky="WE")
        self.entry_n_parcelas.insert(0, self.array_dados[6])
        
        botao_alterar = tk.Button(self.root, text="Alterar Dados", command=self.altera_item_treeview, borderwidth=5, font=("Arial", 14, "bold"), bg="#4CAF50", fg="#ffffff", relief="raised", bd=1)
        botao_alterar.grid(row=7, column=0, columnspan=4, padx=15, pady=10, sticky="NSEW")
        
        
        
        
