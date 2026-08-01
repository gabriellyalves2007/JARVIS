import customtkinter as ctk

from datetime import datetime

from interface.tema import (
    COR_PAINEL,
    COR_PAINEL_CLARO,
    COR_VERDE,
    COR_TEXTO,
    COR_TEXTO_SECUNDARIO,
)


class Header(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            fg_color=COR_PAINEL,
            corner_radius=15,
            height=110
        )

        self.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(20, 10)
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.criar_componentes()
        self.atualizar_data_hora()

    def criar_componentes(self):

        esquerda = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        esquerda.grid(
            row=0,
            column=0,
            padx=22,
            pady=16,
            sticky="w"
        )

        direita = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        direita.grid(
            row=0,
            column=1,
            padx=22,
            pady=16,
            sticky="e"
        )

        self.titulo = ctk.CTkLabel(
            esquerda,
            text="Assistente Virtual Inteligente",
            text_color=COR_TEXTO,
            font=("Segoe UI", 26, "bold")
        )

        self.titulo.pack(anchor="w")

        self.versao = ctk.CTkLabel(
            esquerda,
            text="Build 0.5.0",
            text_color=COR_TEXTO_SECUNDARIO,
            font=("Consolas", 12)
        )

        self.versao.pack(
            anchor="w",
            pady=(6, 0)
        )

        painel_status = ctk.CTkFrame(
            direita,
            fg_color=COR_PAINEL_CLARO,
            corner_radius=10
        )

        painel_status.pack(anchor="e")

        self.status = ctk.CTkLabel(
            painel_status,
            text="● ONLINE",
            text_color=COR_VERDE,
            font=("Segoe UI", 14, "bold")
        )

        self.status.pack(
            padx=14,
            pady=7
        )

        self.data = ctk.CTkLabel(
            direita,
            text="00/00/0000",
            text_color=COR_TEXTO_SECUNDARIO,
            font=("Consolas", 13)
        )

        self.data.pack(
            anchor="e",
            pady=(8, 0)
        )

        self.relogio = ctk.CTkLabel(
            direita,
            text="00:00:00",
            text_color=COR_TEXTO,
            font=("Consolas", 24, "bold")
        )

        self.relogio.pack(anchor="e")

    def atualizar_data_hora(self):
        agora = datetime.now()

        self.data.configure(
            text=agora.strftime("%d/%m/%Y")
        )

        self.relogio.configure(
            text=agora.strftime("%H:%M:%S")
        )

        self.after(
            1000,
            self.atualizar_data_hora
        )