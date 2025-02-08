import tkinter as tk
from tkinter import ttk, messagebox
import re
from datetime import date, datetime
from database import database_connection
from querys import query_obtem_categorias

class RegistroDeGastos:
    def __init__(self, root):
        self.root = root
        self.janelaCadastro()
        
    def janelaCadastro(self):
        """Inicializa a janela de cadastro e seus componentes."""
        self.root.title("Registro de Gastos")

        # Labels and Entries
        self.label_data = tk.Label(self.root, text="Data do Gasto:", font=("Arial", 13, "bold"))
        self.entry_data = tk.Entry(self.root, font="Arial 13", bg="#ffffff", fg="#333333", bd=2, relief="groove")
        self.label_valor = tk.Label(self.root, text="Valor do Gasto:", font=("Arial", 13, "bold"))
        self.entry_valor = tk.Entry(self.root, font="Arial 13", bg="#ffffff", fg="#333333", bd=2, relief="groove")
        self.label_descricao = tk.Label(self.root, text="Descrição:", font=("Arial", 13, "bold"))
        self.entry_descricao = tk.Entry(self.root, font="Arial 13", bg="#ffffff", fg="#333333", bd=2, relief="groove")
        self.label_local = tk.Label(self.root, text="Local:", font=("Arial", 13, "bold"))
        self.entry_local = tk.Entry(self.root, font="Arial 13", bg="#ffffff", fg="#333333", bd=2, relief="groove")
        self.label_forma = tk.Label(self.root, text="Forma Pagamento:", font=("Arial", 13, "bold"))
        self.opcoes_forma = ['Cartão de Crédito', 'Cartão de Débito', 'Dinheiro', 'PIX', 'Saldo da Conta']
        self.combobox_forma = ttk.Combobox(self.root, values=self.opcoes_forma, font="Arial 13")
        self.combobox_forma.configure(background="#ffffff", foreground="#333333")
        self.label_parcelamento = tk.Label(self.root, text='Compra parcelada:', font=("Arial", 13, "bold"))
        self.variavel_opcao = tk.StringVar()
        self.opcao1 = tk.Radiobutton(self.root, text="SIM", variable=self.variavel_opcao, value="SIM", font="Arial 13", bg="#f0f0f0", fg="#333333", selectcolor="#333333")
        self.opcao2 = tk.Radiobutton(self.root, text="NÃO", variable=self.variavel_opcao, value="NÃO", font="Arial 13", bg="#f0f0f0", fg="#333333", selectcolor="#333333",)
        self.label_qtd_parcelas = tk.Label(self.root, text='Quantidade Parcelas:', font=("Arial", 13, "bold"))
        self.spinbox_qtd_parcelas = tk.Spinbox(self.root, from_=0, to=15, font="Arial 13", bg="#ffffff", fg="#333333", bd=2, relief="groove")
        self.label_categoria = tk.Label(self.root, text='Categoria:', font=("Arial", 13, "bold"))
        self.opcoes_categoria = [categoria for categoria in query_obtem_categorias()]
        self.combobox_categoria = ttk.Combobox(self.root, values=self.opcoes_categoria, font="Arial 13")

        # Grid layout
        self.label_data.grid(row=0, column=0, columnspan=1, sticky="W") 
        self.entry_data.grid(row=0, column=1, sticky="WE")
        self.label_valor.grid(row=4, column=0, sticky="W") 
        self.entry_valor.grid(row=4, column=1, sticky="WE")
        self.label_descricao.grid(row=6, column=0, sticky="W")  
        self.entry_descricao.grid(row=6, column=1, sticky="WE")
        self.label_local.grid(row=8, column=0, sticky="W")  
        self.entry_local.grid(row=8, column=1, sticky="WE")
        self.label_forma.grid(row=10, column=0, sticky="W")
        self.combobox_forma.grid(row=10, column=1, sticky="WE")
        self.label_parcelamento.grid(row=12, column=0, sticky="W")
        self.opcao1.grid(row=12, column=1, padx=10, pady=5, sticky="W")
        self.opcao2.grid(row=12, column=1, padx=10, pady=5, sticky="E")  
        self.label_qtd_parcelas.grid(row=14, column=0, sticky="W")      
        self.spinbox_qtd_parcelas.grid(row=14, column=1, sticky="WE") 
        self.label_categoria.grid(row=16, column=0, sticky="W")   
        self.combobox_categoria.grid(row=16, column=1, sticky="WE")
        self.combobox_categoria.configure(background="#ffffff", foreground="#333333")
        self.combobox_forma.configure(background="#ffffff", foreground="#333333")

        # Buttons
        self.botao_registrar = tk.Button(self.root, command=self.insere_info, text="Registrar Gasto", borderwidth=5, font=("Arial", 15, "bold"), bg="#4CAF50", fg="#ffffff", relief="raised", bd=1)
        self.botao_limpar = tk.Button(self.root, command=self.limpa_informacoes, text="Limpar Dados", borderwidth=5, font=("Arial", 15, "bold"), bg="#4CAF50", fg="#ffffff", relief="raised", bd=1)
        self.botao_registrar.grid(row=20, column=0, columnspan=3, sticky="NSEW", pady=(3), padx=3)
        self.botao_limpar.grid(row=24, column=0, columnspan=3, sticky="NSEW", pady=(3), padx=3)

    def obtem_dt_registro(self) -> date:
        """Obtém a data de registro atual."""
        return date.today()

    def obtem_dt_gasto(self) -> str:
        """Obtém e valida a data do gasto."""
        dt_gasto = self.entry_data.get()
        try:
            data_convertida = datetime.strptime(dt_gasto, '%d-%m-%Y').date()
            dt_registro = self.obtem_dt_registro()
            if data_convertida <= dt_registro:
                return data_convertida.strftime('%d-%m-%Y')
            else:
                messagebox.showerror("Erro", "A data do gasto deve ser anterior ou igual à data de registro.")
                return None 
        except ValueError:
            messagebox.showerror("Erro", "Informe uma data válida no formato dd-mm-yyyy.")
            return None  

    def obtem_valor_gasto(self) -> float:
        """Obtém e valida o valor do gasto."""
        valor = self.entry_valor.get()
        padrao = re.compile(r'^\d+(\.\d{1,2})?$')
        if re.match(padrao, valor):
            return float(valor)
        else:
            messagebox.showerror("Erro", "Informe um valor monetário válido!")
            return None

    def obtem_descricao(self) -> str:
        """Obtém e valida a descrição do gasto."""
        descricao = self.entry_descricao.get()
        if isinstance(descricao, str) and descricao.strip() and len(descricao) >= 5:
            return descricao
        else:
            messagebox.showerror("Erro", "Informe uma descrição válida!")
            return None

    def obtem_local(self) -> str:
        """Obtém e valida o local do gasto."""
        local = self.entry_local.get()
        if isinstance(local, str) and local.strip() and len(local) >= 5:
            return local
        else:
            messagebox.showerror("Erro", "Informe um local válido!")
            return None

    def obtem_forma_pagamento(self) -> int:
        """Obtém a forma de pagamento selecionada."""
        forma = self.combobox_forma.get().strip().upper()
        forma_pagamento_map = {
            'CARTÃO DE CRÉDITO': 100,
            'CARTÃO DE DÉBITO': 200,
            'DINHEIRO': 300,
            'PIX': 400,
            'SALDO DA CONTA': 500
        }
        return forma_pagamento_map.get(forma)

    def verifica_parcelamento(self) -> str:
        """Verifica se a compra é parcelada."""
        return 'S' if self.variavel_opcao.get().upper() == 'SIM' else 'N'

    def obtem_qtd_parcelas(self) -> int:
        """Obtém e valida a quantidade de parcelas."""
        try:
            qtd_parcelas = int(self.spinbox_qtd_parcelas.get())
            forma_pagamento = self.obtem_forma_pagamento()
            parcelamento = self.verifica_parcelamento()

            if qtd_parcelas < 0:
                raise ValueError("Informe uma quantidade válida!")
            elif qtd_parcelas > 0 and (forma_pagamento != 100 or parcelamento == 'N'):
                raise ValueError("Verifique as informações de parcelamento inseridas!")
            elif qtd_parcelas == 0 and (forma_pagamento == 100 or parcelamento == 'S'):
                raise ValueError("Verifique as informações de parcelamento inseridas!")
            return qtd_parcelas
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return None

    def obtem_categoria(self) -> int:
        """Obtém a categoria selecionada."""
        categoria = self.combobox_categoria.get()
        categoria_map = query_obtem_categorias()
        return categoria_map.get(categoria)

    def limpa_informacoes(self):
        """Limpa todas as entradas do formulário."""
        self.entry_data.delete(0, 'end')
        self.entry_descricao.delete(0, 'end')
        self.entry_local.delete(0, 'end')
        self.entry_valor.delete(0, 'end')
        self.combobox_forma.set('')
        self.combobox_categoria.set('')
        self.spinbox_qtd_parcelas.delete(0, 'end')

    def verifica_requisicao(self) -> bool:
        """Verifica se todas as informações necessárias foram inseridas corretamente."""
        try:
            return all([
                self.obtem_categoria() is not None,
                self.obtem_qtd_parcelas() is not None,
                self.obtem_forma_pagamento() is not None,
                self.verifica_parcelamento() is not None,
                self.obtem_descricao() is not None,
                self.obtem_valor_gasto() is not None,
                self.obtem_dt_gasto() is not None,
                self.obtem_local() is not None
            ])
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Preencha os campos obrigatórios!")
            return False
            
    def insere_info(self):
        """Insere as informações no banco de dados."""
        connection, cursor = database_connection()
        if connection and cursor and self.verifica_requisicao():
            cursor.execute(
                'INSERT INTO TB_REG_FINANC (DATA_REGISTRO, DATA_GASTO, VALOR, DESCRICAO, LOCAL_GASTO, PARCELAMENTO, N_PARCELAS, IDCATEGORIA, IDFORMA_PAGAMENTO) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (self.obtem_dt_registro(), self.obtem_dt_gasto(), self.obtem_valor_gasto(), self.obtem_descricao(), self.obtem_local(), self.verifica_parcelamento(), self.obtem_qtd_parcelas(), self.obtem_categoria(), self.obtem_forma_pagamento())
            )
            connection.commit()
            connection.close()
        else:
            messagebox.showerror("Erro", "Verifique as informações inseridas!")

