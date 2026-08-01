import customtkinter as ctk

from interface.tema import (
    COR_PAINEL_CLARO,
    COR_VERDE,
    COR_TEXTO_SECUNDARIO,
)


class StatusCard(ctk.CTkFrame):

    def __init__(
        self,
        master,
        titulo: str,
        status: str,
        cor=COR_VERDE
    ):
        super().__init__(
            master,
            fg_color=COR_PAINEL_CLARO,
            corner_radius=10
        )

        self.grid_columnconfigure(1, weight=1)

        self.indicador = ctk.CTkLabel(
            self,
            text="●",
            text_color=cor,
            font=("Segoe UI", 16, "bold")
        )

        self.indicador.grid(
            row=0,
            column=0,
            padx=(15, 8),
            pady=12
        )

        self.titulo = ctk.CTkLabel(
            self,
            text=titulo,
            text_color=COR_TEXTO_SECUNDARIO,
            font=("Segoe UI", 13, "bold")
        )

        self.titulo.grid(
            row=0,
            column=1,
            sticky="w",
            pady=12
        )

        self.status = ctk.CTkLabel(
            self,
            text=status,
            text_color=cor,
            font=("Consolas", 13, "bold")
        )

        self.status.grid(
            row=0,
            column=2,
            sticky="e",
            padx=15,
            pady=12
        )

    def atualizar(
        self,
        status: str,
        cor: str
    ):
        self.status.configure(
            text=status,
            text_color=cor
        )

        self.indicador.configure(
            text_color=cor
        )