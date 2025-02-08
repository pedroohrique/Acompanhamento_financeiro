import tkinter as tk
from querys import obtem_valores
from datetime import datetime
import calendar

class indicadores:
    def __init__(self, root, valor_max):
        self.root = root
        self.valor_max = valor_max 
        valor_total = obtem_valores(tipo_query="TOTAL")
        self.texto_valor_total = f"Total: {valor_total:.2f} R$"
        self.texto_valor_disponivel = f"Valor Disponível: {valor_max - valor_total:.2f} R$"
        self.texto_valor_dia = f"Gasto por dia: {(valor_max - valor_total) / self.calcula_dias_restantes():.2f} R$"
        
    def atualiza_textos(self):
        valor_total = obtem_valores(tipo_query="TOTAL")
        self.texto_valor_total = f"Total: {valor_total:.2f} R$"
        self.texto_valor_disponivel = f"Valor Disponível: {self.valor_max - valor_total:.2f} R$"
        self.texto_valor_dia = f"Gasto por dia: {(self.valor_max - valor_total) / self.calcula_dias_restantes():.2f} R$"   
            
    def calcula_dias_restantes(self):
        dia_atual = datetime.today().day
        mes_atual = datetime.today().month
        ano_atual = datetime.today().year
        qt_dias = calendar.monthrange(ano_atual, mes_atual)
        dias_restantes = (qt_dias[1] - dia_atual)
        return dias_restantes
     
    def setup_indicadores(self):
        if not hasattr(self, 'container_indicadores'):
            self.altura = 30
            self.largura = 1000
            self.container_indicadores = tk.Canvas(self.root, 
                                                bg="green",
                                                width=self.largura,
                                                height=self.altura,
                                                bd=2)
            self.container_indicadores.pack(fill="both", padx=3, pady=4)
            self.texto_indicadores = self.container_indicadores.create_text(
                18, 18, text="", font=("Helvetica", 17, "bold"), fill="white", anchor="w"
            )
        
        self.atualiza_textos()
        self.container_indicadores.itemconfig(
            self.texto_indicadores,
            text=f"{self.texto_valor_total} -- / -- {self.texto_valor_disponivel} -- / -- {self.texto_valor_dia}"
        )
        
        if not hasattr(self, 'scroller_ativo') or not self.scroller_ativo:
            self.scroller_ativo = True
            self.scroller = True
            self.scroller_indicadores()
            
    def scroller_indicadores(self):
        self.velocidade = (-1)
        self.container_indicadores.bind("<Enter>", self.pausar_scroller)
        self.container_indicadores.bind("<Leave>", self.iniciar_scroller)
        
        if self.scroller:
            self.container_indicadores.move(self.texto_indicadores,
                                            self.velocidade,
                                            0)
            pos_x = self.container_indicadores.bbox(self.texto_indicadores)[2]
            if pos_x < 0:
                self.container_indicadores.coords(self.texto_indicadores, self.largura, 20)
                
        if self.scroller_ativo:
            self.root.after(20, self.scroller_indicadores)
            
        
    def pausar_scroller(self, Event):
        self.scroller = False
    
    def iniciar_scroller(self, Event):
        self.scroller = True