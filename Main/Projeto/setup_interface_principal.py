from tkinter import Tk, Toplevel, Menu
from tkinter import ttk, messagebox
from registroGastos import RegistroDeGastos
from database import database_connection
from setup_scroller_indicadores import indicadores
from setup_interface_checklist import checklist
from setup_filtros import filtros
from datetime import datetime
import tkinter as tk    
from setup_interface_edicao_itens import edicao_itens
from querys import query_deleta_item_treeview
from robo_coleta import robo_coleta_dados

class App:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Acompanhamento Financeiro - {datetime.today().year}")
        self.root.configure(bg="lightgrey")
        self.obj_indicadores = indicadores(self.root, 7050)
        self.obj_checklist = checklist(root=self.root)
        self.obj_filtros = filtros(root=self.root)
        self.frame_treeview = tk.Frame(self.root, bd=2, relief="solid")
        self.frame_treeview.pack(fill="both", expand=True, padx=5, pady=(5, 0))
        self.obj_filtros.entry_filtro_valor.bind("<KeyRelease>", self.lista_dados_treeview)
        self.obj_filtros.entry_filtro_dt_compra.bind("<KeyRelease>", self.lista_dados_treeview)
        self.obj_filtros.entry_filtro_dt_vencimento.bind("<KeyRelease>", self.lista_dados_treeview)
        self.setup_menu()
        self.setup_treeview()
        self.atualiza_interface()
        self.treeview.bind("<Double-1>", self.editaDados_treeview)
        
    def atualiza_interface(self):
        self.lista_dados_treeview()
        self.obj_indicadores.setup_indicadores()
        
    def setup_menu(self):
        self.menu_barra = Menu(self.root)
        self.root.configure(menu=self.menu_barra)
        self.menu_opcoes = Menu(self.menu_barra, tearoff=0)
        self.menu_barra.add_cascade(label="Menu Opções", menu=self.menu_opcoes)
        self.menu_opcoes.add_command(label="Registrar gasto", command=self.registro_gasto)
        self.menu_opcoes.add_command(label="Coleta de Registros", command=robo_coleta_dados)
        #self.menu_opcoes.add_command(label="Dashboard", command=self.dashboard_financeiro)
        self.menu_opcoes.add_command(label="Atualizar", command=self.lista_dados_treeview)
        self.menu_opcoes.add_command(label="Contas a Pagar", command=self.obj_checklist.setup_treeview)
        self.menu_opcoes.add_command(label="Sair", command=self.root.destroy)

    def setup_treeview(self):
        style = ttk.Style()
        style.theme_use("winnative")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), bg="white")
        style.configure("Treeview", font=("Arial", 11), bg="white", width=2000)

        columns = ["DT_COMPRA", "DT_PAGAMENTO", "VALOR_TOTAL", "VALOR_PARCELA", "VALOR_PENDENTE", "CATEGORIA", "DESCRICAO", "LOCAL_GASTO"]
        headings = ["Data", "Vencimento", "Total", "Parcela", "Pendente", "Categoria", "Descrição", "Local"]
        widths = [80, 100, 80, 80, 80, 150, 150, 150]

        self.treeview = ttk.Treeview(self.frame_treeview, style="Treeview", columns=columns, show="headings", height=20)
        self.treeview.pack(padx=5, pady=5, fill="both", expand=True)

        for col, heading, width in zip(columns, headings, widths):
            self.treeview.heading(col, text=heading, anchor="center")
            self.treeview.column(col, width=width, anchor="center")     
        
    def registro_gasto(self):
        janela_cadastro = Toplevel(self.root)
        janela_cadastro.protocol("WM_DELETE_WINDOW", lambda: [janela_cadastro.destroy(), self.lista_dados_treeview(), self.obj_indicadores.setup_indicadores()])
        RegistroDeGastos(janela_cadastro)
        self.obj_indicadores.setup_indicadores()
        
    def lista_dados_treeview(self, Event=None):
        for index in self.treeview.get_children():
            self.treeview.delete(index)
        
        valores = self.obj_filtros.obtem_valores_filtros()    
        connection, cursor = database_connection()
        
        if valores is not None:
            query = """
            SELECT
                CONVERT(VARCHAR, AF.DT_COMPRA, 103) AS "DT Compra",
                CONVERT(VARCHAR, AF.DT_PAGAMENTO, 103) AS "DT Pagamento",
                AF.VALOR_TOTAL AS "Total",
                AF.VALOR_PARCELA AS "Valor Parcela",
                AF.VALOR_PENDENTE AS "Valor Pendente",
                C.DESCRICAO AS "Categoria",
                RF.DESCRICAO AS "Descrição",
                RF.LOCAL_GASTO AS "Local",
                RF.ID_REGISTRO AS "IDREGISTRO",
                FP.DESCRICAO,
                RF.PARCELAMENTO,
				RF.N_PARCELAS
            FROM 
                TB_ACOMPANHAMENTO_FINANC AF
                JOIN TB_CATEGORIA C ON AF.IDCATEGORIA = C.ID_CATEGORIA
                JOIN TB_REG_FINANC RF ON AF.IDREGISTRO = RF.ID_REGISTRO
                JOIN TB_FORMA_PAGAMENTO FP ON RF.IDFORMA_PAGAMENTO = FP.ID_FORMA"""
                
            conditions = []
            params = []
            
            if valores.get("ValorCompra"):
                conditions.append("AF.VALOR_TOTAL = ?")
                params.append(valores.get("ValorCompra"))
                
            if valores.get("DTCompra"):
                conditions.append("AF.DT_COMPRA = ?")
                params.append(valores.get("DTCompra"))
            
            if valores.get("DTVencimento"):
                conditions.append("AF.DT_PAGAMENTO = ?")
                params.append(valores.get("DTVencimento"))
                
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY AF.DT_COMPRA DESC"
            cursor.execute(query, params)            
        else:
            query = """
            SELECT
                CONVERT(VARCHAR, AF.DT_COMPRA, 103) AS "DT Compra",
                CONVERT(VARCHAR, AF.DT_PAGAMENTO, 103) AS "DT Pagamento",
                AF.VALOR_TOTAL "Total",
                AF.VALOR_PARCELA "Valor Parcela",
                AF.VALOR_PENDENTE "Valor Pendente",
                C.DESCRICAO "Categoria",
                RF.DESCRICAO "Descrição",
                RF.LOCAL_GASTO "Local",
                RF.ID_REGISTRO "IDREGISTRO",
                FP.DESCRICAO,
                RF.PARCELAMENTO,
				RF.N_PARCELAS
            FROM 
                TB_ACOMPANHAMENTO_FINANC AF
                JOIN TB_CATEGORIA C ON AF.IDCATEGORIA = C.ID_CATEGORIA
                JOIN TB_REG_FINANC RF ON AF.IDREGISTRO = RF.ID_REGISTRO
                JOIN TB_FORMA_PAGAMENTO FP ON RF.IDFORMA_PAGAMENTO = FP.ID_FORMA
            WHERE
                MONTH(AF.DT_PAGAMENTO) >= ?
            ORDER BY
                AF.DT_COMPRA DESC"""
            cursor.execute(query, (datetime.today().month,))
            
        retorno_query = cursor.fetchall()
        
        for item in retorno_query:
            self.treeview.insert("", "end", values=(item[0], item[1], str(item[2]) + " " + "R$", str(item[3]) + " " + "R$", str(item[4]) + " " + "R$", item[5], item[6], item[7], item[8], item[9], item[10], item[11]))
        connection.commit()
        connection.close()
    
      
    def editaDados_treeview(self, event): 
        
        def exibe_janela_edicao():
            obj_edicao = edicao_itens(array_dados=[self.valores[0], self.valores[2], self.valores[5], self.valores[6], self.valores[9], self.valores[10], self.valores[11], self.valores[8]])
            return obj_edicao.janela_edicao()
    
        def deleta_item():
            id_registro = self.valores[8]
            confirmacao = messagebox.askquestion("Atenção", f"Confirmar exclusção do registro: {id_registro}?")
            query_deleta_item_treeview(id_registro=id_registro) if confirmacao == "yes" else messagebox.showinfo("Atenção", f"Registro {id_registro} não foi excluído!") 
            
        try:  
            registro_selecionado = self.treeview.selection()[0]
            if registro_selecionado:
                self.valores = self.treeview.item(registro_selecionado)['values']
                eixo_x, eixo_y, largura, altura = self.treeview.bbox(registro_selecionado)       
                x_root = self.treeview.winfo_rootx() + eixo_x
                y_root = self.treeview.winfo_rooty() + eixo_y + altura
                janela_botoes = Toplevel(self.frame_treeview)
                janela_botoes.geometry(f"100x50+{x_root}+{y_root}")
                janela_botoes.overrideredirect(True)
                tk.Button(janela_botoes, text="Alterar", font=("Helvetica", 9, "bold"), fg="green", command=lambda:[janela_botoes.destroy(), exibe_janela_edicao(), self.atualiza_interface()]).pack(fill=tk.BOTH, expand=True)
                tk.Button(janela_botoes, text="Excluir", font=("Helvetica", 9, "bold"), fg="red", command=lambda:[janela_botoes.destroy(), deleta_item(), self.atualiza_interface()]).pack(fill=tk.BOTH, expand=True)
                
                def close_window(event):
                    janela_botoes.destroy() 

            root.bind("<Button-1>", close_window)
              
        except IndexError:
            messagebox.showerror("Erro", "Nenhum item foi selecionado!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()


