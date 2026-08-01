import socket

import customtkinter as ctk
import psutil

from interface.tema import (
    COR_PAINEL,
    COR_CIANO,
    COR_VERDE,
    COR_TEXTO_SECUNDARIO,
)

from interface.widgets.core_widget import CoreWidget
from interface.widgets.progress_card import ProgressCard
from interface.widgets.status_card import StatusCard


COR_ERRO = "#FF4D4D"


class Dashboard(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            fg_color=COR_PAINEL,
            corner_radius=15
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.criar_componentes()
        self.atualizar_sistema()

    def criar_componentes(self):
        self.conteudo = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )

        self.conteudo.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )

        self.conteudo.grid_columnconfigure(0, weight=1)

        self.core_widget = CoreWidget(self.conteudo)

        self.core_widget.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=15,
            pady=(15, 10)
        )

        self.cpu_card = ProgressCard(
            self.conteudo,
            titulo="CPU",
            valor=0,
            cor=COR_VERDE
        )

        self.cpu_card.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=15,
            pady=5
        )

        self.memoria_card = ProgressCard(
            self.conteudo,
            titulo="MEMÓRIA",
            valor=0,
            cor=COR_CIANO
        )

        self.memoria_card.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=15,
            pady=5
        )

        self.internet_card = StatusCard(
            self.conteudo,
            titulo="INTERNET",
            status="VERIFICANDO",
            cor=COR_TEXTO_SECUNDARIO
        )

        self.internet_card.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=15,
            pady=5
        )

        self.ia_card = StatusCard(
            self.conteudo,
            titulo="IA",
            status="ATIVA",
            cor=COR_CIANO
        )

        self.ia_card.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=15,
            pady=5
        )

        self.microfone_card = StatusCard(
            self.conteudo,
            titulo="MICROFONE",
            status="EM ESPERA",
            cor=COR_TEXTO_SECUNDARIO
        )

        self.microfone_card.grid(
            row=5,
            column=0,
            sticky="ew",
            padx=15,
            pady=(5, 15)
        )

    def verificar_internet(self):
        conexao = None

        try:
            conexao = socket.create_connection(
                ("8.8.8.8", 53),
                timeout=2
            )

            self.internet_card.atualizar(
                status="ONLINE",
                cor=COR_VERDE
            )

        except OSError:
            self.internet_card.atualizar(
                status="OFFLINE",
                cor=COR_ERRO
            )

        finally:
            if conexao is not None:
                conexao.close()

    def atualizar_sistema(self):
        uso_cpu = psutil.cpu_percent(interval=None)
        uso_memoria = psutil.virtual_memory().percent

        self.cpu_card.atualizar(uso_cpu)
        self.memoria_card.atualizar(uso_memoria)

        self.verificar_internet()

        self.after(
            5000,
            self.atualizar_sistema
        )