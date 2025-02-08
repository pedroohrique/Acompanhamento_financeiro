import tkinter as tk 

class filtros:
    def __init__(self, root):
        self.root = root
        self.setup_filtro_de_pesquisa()
        
    def setup_filtro_de_pesquisa(self):
        self.frame_filtros = tk.Frame(self.root, bd=2, relief="solid")
        self.frame_filtros.pack(fill="both", expand=True, padx=5, pady=(5,0))
        
        #Instanciando os labels
        label_filtro_valor = tk.Label(self.frame_filtros,
                                      text="Valor gasto:",
                                      font=("Arial", 12, "bold"))
        label_filtro_dt_compra = tk.Label(self.frame_filtros,
                                     text="Data gasto:",
                                     font=("Arial", 12, "bold"))
        label_filtro_dt_vencimento = tk.Label(self.frame_filtros,
                                              text="Data vencimento:",
                                              font=("Arial", 12, "bold"))
        
        #Posicionamento dos Labels
        label_filtro_valor.grid(row=0, column=0, padx=8, pady=6, sticky="w")
        label_filtro_dt_compra.grid(row=0, column=2, padx=8, pady=6, sticky="w")
        label_filtro_dt_vencimento.grid(row=0, column=4, padx=8, pady=6, sticky="w")
        
        #Criação dos entrys
        self.entry_filtro_valor = tk.Entry(self.frame_filtros,
                                           font=("Arial", 12), 
                                           bg="#FFFFFF", 
                                           fg="#333333", 
                                           bd=2, 
                                           relief="solid")
        self.entry_filtro_dt_compra = tk.Entry(self.frame_filtros,
                                        font=("Arial", 12), 
                                        bg="#FFFFFF", 
                                        fg="#333333", 
                                        bd=2, 
                                        relief="solid" )
        self.entry_filtro_dt_vencimento = tk.Entry(self.frame_filtros,
                                                   font=("Arial", 12),
                                                   bg="#FFFFFF",
                                                   fg="#333333",
                                                   bd=2,
                                                   relief="solid")
        
        #Posicionamento dos Entrys
        self.entry_filtro_valor.grid(row=0, column=1, padx=8, pady=6, sticky="w")
        self.entry_filtro_dt_compra.grid(row=0, column=3, padx=8, pady=6, sticky="w")
        self.entry_filtro_dt_vencimento.grid(row=0, column=5, padx=8, pady=6, sticky="w")
        
  
        
    
    def obtem_valores_filtros(self, Event=None):
        valor_compra = self.entry_filtro_valor.get().strip()
        dt_compra = self.entry_filtro_dt_compra.get().strip()
        dt_vencimento = self.entry_filtro_dt_vencimento.get().strip()
        
        if not valor_compra and not dt_compra and not dt_vencimento:
            return None
        
        else:
            valores = {"ValorCompra": valor_compra,
                       "DTCompra": dt_compra,
                       "DTVencimento": dt_vencimento}

            return valores