import time

import customtkinter as ctk

from interface.tema import (
    COR_PAINEL_CLARO,
    COR_CIANO,
    COR_TEXTO,
)

from interface.widgets.info_card import InfoCard


class CoreWidget(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            fg_color=COR_PAINEL_CLARO,
            corner_radius=18
        )

        self.tempo_inicio = time.time()

        self.grid_columnconfigure(0, weight=1)

        self.criar_componentes()
        self.atualizar_tempo_ativo()

    def criar_componentes(self):
        self.nucleo = ctk.CTkFrame(
            self,
            width=170,
            height=170,
            corner_radius=85,
            fg_color="#10263A",
            border_width=3,
            border_color=COR_CIANO
        )

        self.nucleo.grid(
            row=0,
            column=0,
            padx=20,
            pady=(20, 15)
        )

        self.nucleo.grid_propagate(False)

        self.estado_visual = ctk.CTkLabel(
            self.nucleo,
            text="◉",
            text_color=COR_CIANO,
            font=("Segoe UI", 56)
        )

        self.estado_visual.place(
            relx=0.5,
            rely=0.38,
            anchor="center"
        )

        self.nome = ctk.CTkLabel(
            self.nucleo,
            text="JARVIS",
            text_color=COR_TEXTO,
            font=("Segoe UI", 20, "bold")
        )

        self.nome.place(
            relx=0.5,
            rely=0.70,
            anchor="center"
        )

        self.estado_card = InfoCard(
            self,
            titulo="ESTADO",
            valor="EM ESPERA"
        )

        self.estado_card.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=15,
            pady=5
        )

        self.ultima_acao_card = InfoCard(
            self,
            titulo="ÚLTIMA AÇÃO",
            valor="Aguardando"
        )

        self.ultima_acao_card.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=15,
            pady=5
        )

        self.tempo_card = InfoCard(
            self,
            titulo="TEMPO ATIVO",
            valor="00:00:00"
        )

        self.tempo_card.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=15,
            pady=(5, 15)
        )

    def alterar_estado(
        self,
        estado: str,
        mensagem: str,
        cor: str
    ):
        self.estado_visual.configure(
            text_color=cor
        )

        # O nome central permanece sempre como JARVIS.
        self.nome.configure(
            text="JARVIS"
        )

        self.estado_card.atualizar(
            estado.upper()
        )

        self.ultima_acao_card.atualizar(
            mensagem
        )

    def atualizar_tempo_ativo(self):
        segundos_totais = int(
            time.time() - self.tempo_inicio
        )

        horas = segundos_totais // 3600
        minutos = (segundos_totais % 3600) // 60
        segundos = segundos_totais % 60

        tempo_formatado = (
            f"{horas:02d}:"
            f"{minutos:02d}:"
            f"{segundos:02d}"
        )

        self.tempo_card.atualizar(
            tempo_formatado
        )

        self.after(
            1000,
            self.atualizar_tempo_ativo
        )