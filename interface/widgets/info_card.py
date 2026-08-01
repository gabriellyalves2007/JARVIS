import customtkinter as ctk

from interface.tema import (
    COR_PAINEL_CLARO,
    COR_TEXTO,
    COR_TEXTO_SECUNDARIO,
)


class InfoCard(ctk.CTkFrame):

    def __init__(
        self,
        master,
        titulo: str,
        valor: str
    ):
        super().__init__(
            master,
            fg_color=COR_PAINEL_CLARO,
            corner_radius=10
        )

        self.grid_columnconfigure(1, weight=1)

        self.label_titulo = ctk.CTkLabel(
            self,
            text=titulo,
            text_color=COR_TEXTO_SECUNDARIO,
            font=("Segoe UI", 13, "bold")
        )

        self.label_titulo.grid(
            row=0,
            column=0,
            padx=15,
            pady=12,
            sticky="w"
        )

        self.label_valor = ctk.CTkLabel(
            self,
            text=valor,
            text_color=COR_TEXTO,
            font=("Consolas", 13, "bold")
        )

        self.label_valor.grid(
            row=0,
            column=1,
            padx=15,
            pady=12,
            sticky="e"
        )

    def atualizar(self, novo_valor: str):
        self.label_valor.configure(
            text=novo_valor
        )