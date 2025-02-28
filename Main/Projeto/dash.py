
from querys import obtem_valores, gasto_por_categoria, obtem_aplicacao_financ, dados_grafico_aplicacaoFinanc, dados_grafico_gastoMensal
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import ttkbootstrap as ttk
import pandas as pd
from datetime import datetime
import calendar

class dashboard:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1375x850")
        self.root.resizable(False, False)
        self.style = ttk.Style()
        self.style.configure("Custom.TFrame",
                borderwidth=2,   # Define a espessura da borda
                relief="solid")
        self.style_texto = ("Helvetica", 
                       16, 
                       "bold")
        self.largura_frame_indicadores = 225
        self.altura_frame_indicadores = 100
        self.espacamento_indicadores = 3
        self.largua_frame_categoria = 300
        self.altura_frame_categoria = 520
        
        
        self.grafico()
        self.configura_frames()
        
    def calcula_dias_restantes(self):
        dia_atual = datetime.today().day
        mes_atual = datetime.today().month
        ano_atual = datetime.today().year
        qt_dias = calendar.monthrange(ano_atual, mes_atual)
        dias_restantes = (qt_dias[1] - dia_atual)
        return dias_restantes if dias_restantes > 0 else 1


    def obtem_valor_indicadores(self, valor_max) -> dict:
            valor_total = float(obtem_valores(tipo_query="TOTAL"))
            valor_disponivel = float((valor_max - valor_total))
            valor_cartao_credito = float(obtem_valores(tipo_query="CARTAO"))
            valor_deb_pix = float(obtem_valores(tipo_query="OUTROS"))
            valor_diario = float((valor_max - valor_total) / self.calcula_dias_restantes())
            
            dict_dados = {
                "V_TOTAL" : valor_total,
                "V_DISPONIVEL": valor_disponivel,
                "V_CARTAO" : valor_cartao_credito,
                "V_DEB_PIX" : valor_deb_pix,
                "V_DIARIO" : valor_diario
            }

            return dict_dados
    
    def configura_cor_indicadores(self, frame: str, valor_frame: float, valor_max: float):
        if frame in ("TG", "CDC", "DEP", "GD") and valor_frame != 0:
                porcentagem = (valor_frame / valor_max) * 100
                cor = (
                        "lime" if porcentagem <= 50 else
                        "yellow" if porcentagem <= 75 else
                        "red"
                )
                return cor
                
        if frame == "VD" and valor_frame !=0:
                porcentagem = (valor_frame / valor_max) * 100
                cor = (
                        "lime" if porcentagem >= 75 else
                        "yellow" if porcentagem >= 50 else
                        "red"
                )
                return cor
         
    def configura_frames(self):     
        dados_indicadores = self.obtem_valor_indicadores(valor_max=7050.00)
        valor_categorias = gasto_por_categoria()
        #Configuração dos frames                
        #Orçamento Mensal---------------------------------------------------------------------------
        frame_OM = ttk.Frame(self.root, padding=10, style="Custom.TFrame")
        frame_OM.place(x=5, y=5, height=self.altura_frame_indicadores, width=self.largura_frame_indicadores)


        #Total Gasto-------------------------------------------------------------------------------
        frame_TG = ttk.Frame(self.root, padding=10, style="Custom.TFrame")
        frame_TG.place(x=self.largura_frame_indicadores + 8, 
                       y=5, 
                       height=self.altura_frame_indicadores, 
                       width=self.largura_frame_indicadores)


        #Frame Valor Disponivel--------------------------------------------------------------------------
        frame_VD = ttk.Frame(self.root, padding=10, style="Custom.TFrame")
        frame_VD.place(x=(int(frame_TG.place_info()['x']) + self.largura_frame_indicadores + self.espacamento_indicadores), 
                       y=5, 
                       height=self.altura_frame_indicadores, 
                       width=self.largura_frame_indicadores)

        #Frame Gasto Cartão de Crédito-------------------------------------------------------------------
        frame_CDC = ttk.Frame(self.root, padding=10, style="Custom.TFrame")
        frame_CDC.place(x=(int(frame_VD.place_info()['x']) + self.largura_frame_indicadores + self.espacamento_indicadores), 
                        y=5, 
                        height=self.altura_frame_indicadores, 
                        width=self.largura_frame_indicadores)
        
        #Frame Gastos Débito e Pix
        frame_DEP = ttk.Frame(self.root, padding=10, style="Custom.TFrame")
        frame_DEP.place(x=(int(frame_CDC.place_info()['x']) + self.largura_frame_indicadores + self.espacamento_indicadores), 
                        y=5, 
                        height=self.altura_frame_indicadores, 
                        width=self.largura_frame_indicadores)
        
        #Frame Gasto Diário
        frame_GD = ttk.Frame(self.root, padding=10, style="Custom.TFrame")
        frame_GD.place(x=(int(frame_DEP.place_info()['x']) + self.largura_frame_indicadores + self.espacamento_indicadores), 
                       y=5, 
                       height=self.altura_frame_indicadores, 
                       width=self.largura_frame_indicadores)
        
        frame_CAT = ttk.Frame(self.root, 
                              padding=10, 
                              style="Custom.TFrame")
        frame_CAT.place(x=5, 
                        y=(int(frame_OM.place_info()['height']) + 15),
                        width=self.largua_frame_categoria,
                        height=self.altura_frame_categoria)
        
        frame_POU = ttk.Frame(self.root, padding=10, style="Custom.TFrame")
        frame_POU.place(x=5, 
                        y=(int(frame_CAT.place_info()["height"]) + 125),
                        width=self.largua_frame_categoria,
                        height=200)
        #Configuração dos labels        
        #Orçamento Mensal----------------------------------------------------------------------------
        label_texto_OM = ttk.Label(frame_OM, text="Orçamento Mensal", font=self.style_texto)
        label_valor_OM = ttk.Label(frame_OM, text=f"R$ 7050,00", font=self.style_texto)
        label_texto_OM.pack()
        label_valor_OM.pack(pady=15)

        
        #Total Gasto-------------------------------------------------------------------------------
        label_texto_TG = ttk.Label(frame_TG, text="Total Gasto", font=self.style_texto)
        label_valor_TG = ttk.Label(frame_TG, 
                                   text=f"R$ {dados_indicadores['V_TOTAL']:.2f}", 
                                   font=self.style_texto, 
                                   foreground=self.configura_cor_indicadores("TG", dados_indicadores['V_TOTAL'], 7050.00))
        label_texto_TG.pack()
        label_valor_TG.pack(pady=15)

        #Valor Disponivel--------------------------------------------------------------------------
        label_texto_VD = ttk.Label(frame_VD, text="Valor Disponível", font=self.style_texto)
        label_valor_VD = ttk.Label(frame_VD, 
                                   text=f"R$ {dados_indicadores['V_DISPONIVEL']:.2f}", 
                                   font=self.style_texto,
                                   foreground=self.configura_cor_indicadores("VD", dados_indicadores['V_DIARIO'], 7050.00))
        label_texto_VD.pack()
        label_valor_VD.pack(pady=15)
        
        #Gastos Cartão de crédito
        label_texto_CDC = ttk.Label(frame_CDC, text="Cartão de Crédito", font=self.style_texto)
        label_valor_CDC = ttk.Label(frame_CDC, 
                                    text=f"R$ {dados_indicadores['V_CARTAO']:.2f}", 
                                    font=self.style_texto,
                                    foreground=self.configura_cor_indicadores("CDC", dados_indicadores['V_CARTAO'], 7050.00))
        label_texto_CDC.pack()
        label_valor_CDC.pack(pady=15)
        
        #Gastos Débito e PIX
        label_texto_DEP = ttk.Label(frame_DEP, text="Débito / PIX", font=self.style_texto)
        label_valor_DEP = ttk.Label(frame_DEP, 
                                    text=f"R$ {dados_indicadores['V_DEB_PIX']:.2f}", 
                                    font=self.style_texto,
                                    foreground=self.configura_cor_indicadores("DEP", dados_indicadores['V_DEB_PIX'], 7050.00))
        label_texto_DEP.pack()
        label_valor_DEP.pack(pady=15)
        
        #Gasto Diário
        label_texto_GD = ttk.Label(frame_GD, text="Gasto Diário", font=self.style_texto)
        label_valor_GD = ttk.Label(frame_GD, 
                                   text=f"R$ {dados_indicadores['V_DIARIO']:.2f}", 
                                   font=self.style_texto,
                                   foreground=self.configura_cor_indicadores("GD", dados_indicadores['V_TOTAL'], 7050.00))
        label_texto_GD.pack()
        label_valor_GD.pack(pady=15)
        
        #Gasto por Categoria - labels
        
        label_titulo_CAT = ttk.Label(frame_CAT, text="Gastos por Categoria", font=("Helvetica", 16, "bold"), foreground="blue")
        label_titulo_CAT.grid(row=0, column=0, padx=30, pady=5, sticky="nsew")
        
        #Alimentação       
        label_cat_AL = ttk.Label(frame_CAT, text="Alimentação",  font=("Helvetica", 12, "bold"))
        label_cat_AL.grid(row=1, column=0, pady=10, sticky="w")
        
        label_valor_AL = ttk.Label(frame_CAT, text=f"R$ {valor_categorias[100]}",font=("Helvetica", 12, "bold"))
        label_valor_AL.grid(row=1, column=0, pady=10, sticky="e")
        
        #Compras
        label_cat_CO = ttk.Label(frame_CAT, text="Compras",  font=("Helvetica", 12, "bold"))
        label_cat_CO.grid(row=2, column=0, pady=10, sticky="w")
        
        label_valor_CO = ttk.Label(frame_CAT, text=f"R$ {valor_categorias[600]}",font=("Helvetica", 12, "bold"))
        label_valor_CO.grid(row=2, column=0, pady=10, sticky="e")
        
        #Moradia
        label_cat_MO = ttk.Label(frame_CAT, text="Moradia",  font=("Helvetica", 12, "bold"))
        label_cat_MO.grid(row=3, column=0, pady=10, sticky="w")
        
        label_valor_MO = ttk.Label(frame_CAT, text=f"R$ {valor_categorias[200]}",font=("Helvetica", 12, "bold"))
        label_valor_MO.grid(row=3, column=0, pady=10, sticky="e")
        
        #Transporte
        label_cat_TR = ttk.Label(frame_CAT, text="Transporte",  font=("Helvetica", 12, "bold"))
        label_cat_TR.grid(row=4, column=0, pady=10, sticky="w")
        
        label_valor_TR = ttk.Label(frame_CAT, text=f"R$ {valor_categorias[300]}",font=("Helvetica", 12, "bold"))
        label_valor_TR.grid(row=4, column=0, pady=10, sticky="e")
        
        #Saúde
        label_cat_saude = ttk.Label(frame_CAT, text="Saúde",  font=("Helvetica", 12, "bold"))
        label_cat_saude.grid(row=5, column=0, pady=10, sticky="w")
        
        label_valor_SA = ttk.Label(frame_CAT, text=f"R$ {valor_categorias[400]}",font=("Helvetica", 12, "bold"))
        label_valor_SA.grid(row=5, column=0, pady=10, sticky="e")
        
        #Lazer e Entreterimento
        label_cat_LE = ttk.Label(frame_CAT, text="Lazer",  font=("Helvetica", 12, "bold"))
        label_cat_LE.grid(row=6, column=0, pady=10, sticky="w")
        
        label_valor_LE = ttk.Label(frame_CAT, text=f"R$ {valor_categorias[500]}",font=("Helvetica", 12, "bold"))
        label_valor_LE.grid(row=6, column=0, pady=10, sticky="e")
        
        #Gastos Ocasionais
        label_cat_GO = ttk.Label(frame_CAT, text="Gastos Ocasionais",  font=("Helvetica", 12, "bold"))
        label_cat_GO.grid(row=7, column=0, pady=10, sticky="w")
        
        label_valor_GO = ttk.Label(frame_CAT, text=f"R$ {valor_categorias[700]}",font=("Helvetica", 12, "bold"))
        label_valor_GO.grid(row=7, column=0, pady=10, sticky="e")
        
        #Investimentos
        label_cat_IN = ttk.Label(frame_CAT, text="Investimentos",  font=("Helvetica", 12, "bold"))
        label_cat_IN.grid(row=8, column=0, pady=10, sticky="w")
        
        label_valor_IN = ttk.Label(frame_CAT, text=f"R$ {valor_categorias[800]}",font=("Helvetica", 12, "bold"))
        label_valor_IN.grid(row=8, column=0, pady=10, sticky="e")
        
        #Pagamento Fatura
        label_cat_PF = ttk.Label(frame_CAT, text="Pagamento Fatura",  font=("Helvetica", 12, "bold"))
        label_cat_PF.grid(row=9, column=0, pady=10, sticky="w")
        
        label_valor_PF = ttk.Label(frame_CAT, text=f"R$ {valor_categorias[900]}",font=("Helvetica", 12, "bold"))
        label_valor_PF.grid(row=9, column=0, pady=10, sticky="e")
        
        #Educação
        label_cat_PF = ttk.Label(frame_CAT, text="Educação",  font=("Helvetica", 12, "bold"))
        label_cat_PF.grid(row=10, column=0, pady=10, sticky="w")
        
        label_valor_PF = ttk.Label(frame_CAT, text=f"R$ {valor_categorias[1000]}",font=("Helvetica", 12, "bold"))
        label_valor_PF.grid(row=10, column=0, pady=10, sticky="e")
        
        #Outros
        label_cat_OU = ttk.Label(frame_CAT, text="Outros",  font=("Helvetica", 12, "bold"))
        label_cat_OU.grid(row=11, column=0, pady=10, sticky="w")
        
        label_valor_OU = ttk.Label(frame_CAT, text=f"R$ {valor_categorias[1100]}",font=("Helvetica", 12, "bold"))
        label_valor_OU.grid(row=11, column=0, pady=10, sticky="e")
        
        label_titulo_investimento = ttk.Label(frame_POU, text="Valor Investido M-1", font=("Helvetica", 20, "bold"), foreground="green")
        label_valor_investido =ttk.Label(frame_POU, text=f"R$ {obtem_aplicacao_financ()}", font=("Helvetica", 32, "bold"), foreground="lime")
        label_titulo_investimento.grid(row=0, column=0, padx=12, pady=5, sticky="nsew")
        label_valor_investido.grid(row=5, column=0, padx=10, pady=30, sticky="nsew")
        #print(f"A largura do frame é: {frame_OM.place_info()['x']}")

    
        
    def grafico(self):
        frame_grafico_gasto = ttk.Frame(self.root, padding=10, style="Custom.TFrame")
        frame_grafico_gasto.place(x=(int(self.largua_frame_categoria) + 15),
                                y=(int(self.altura_frame_indicadores) + 15),
                                width=1055,
                                height=363)
        frame_grafico_aplicacoes = ttk.Frame(self.root, padding=10, style="Custom.TFrame")
        frame_grafico_aplicacoes.place(x=(int(self.largua_frame_categoria) + 15),
                                    y=(int(frame_grafico_gasto.place_info()['height']) + int(self.altura_frame_indicadores) + 20),
                                    width=1055,
                                    height=363)

        valores_grafico_aplicacao = dados_grafico_aplicacaoFinanc()
        valores_grafico_gastos = dados_grafico_gastoMensal()
        
        dataframe_financ = pd.DataFrame(valores_grafico_aplicacao)
       
        dataframe_gastosMensais = pd.DataFrame(valores_grafico_gastos)

        # Gráfico 1 (Investimentos e Aplicações)
        fig, ax = plt.subplots(figsize=(9, 4))
        fig.patch.set_facecolor('grey')  # Fundo do gráfico
        ax.set_facecolor('dimgray')  # Fundo dos eixos

        sns.barplot(data=dataframe_financ, x="Mês", y="Valores", ax=ax, color='green')
        ax.set_title("Evolução - Investimentos e Aplicações", color='white')
        ax.set_ylim(0, dataframe_financ['Valores'].max() * 1.15)
        ax.tick_params(colors='white')  # Cor dos ticks
        ax.xaxis.label.set_color('white')  # Cor do label do eixo X
        ax.yaxis.label.set_color('white')  # Cor do label do eixo Y
        
        for i, (x, y) in enumerate(zip(dataframe_financ['Mês'], dataframe_financ['Valores'])):
            ax.text(x, y, f"R$ {y:.2f}", color='white', fontsize=10, ha='center', va='bottom')

        ax.grid(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        plt.tight_layout()
        plt.close(fig)

        canvas = FigureCanvasTkAgg(fig, master=frame_grafico_aplicacoes)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)
        #--------------------------------------------------------------------------------------------------
        # Gráfico 2 (Gastos Mensais)
        fig, ax = plt.subplots(figsize=(9, 4))
        fig.patch.set_facecolor('gray')
        ax.set_facecolor('dimgray')

        sns.barplot(data=dataframe_gastosMensais, x="Mês", y="Valores", ax=ax, color='firebrick')
        ax.set_title("Evolução - Gastos Mensais", color='white')
        ax.set_ylim(0, dataframe_gastosMensais['Valores'].max() * 1.1)
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        
        for i, (x,y) in enumerate(zip(dataframe_gastosMensais['Mês'], dataframe_gastosMensais["Valores"])):
            ax.text(x, y, f"R$ {y:.2f}", color='white', fontsize=10, ha='center', va='bottom')

        ax.grid(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        plt.tight_layout()
        plt.close(fig)

        canvas = FigureCanvasTkAgg(fig, master=frame_grafico_gasto)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)
    
        
if __name__=="__main__":
    root = ttk.Window(themename="solar")
    app = dashboard(root)
    root.title("Dashboard Financeiro 2025")
    root.mainloop()
    
