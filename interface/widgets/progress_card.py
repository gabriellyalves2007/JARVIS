import customtkinter as ctk

from interface.tema import (
    COR_PAINEL_CLARO,
    COR_CIANO,
    COR_TEXTO,
    COR_TEXTO_SECUNDARIO
)


class ProgressCard(ctk.CTkFrame):

    def __init__(
        self,
        master,
        titulo: str,
        valor: float = 0,
        cor=COR_CIANO
    ):
        super().__init__(
            master,
            fg_color=COR_PAINEL_CLARO,
            corner_radius=10
        )

        self.cor = cor

        self.grid_columnconfigure(0, weight=1)

        self.titulo = ctk.CTkLabel(
            self,
            text=titulo,
            text_color=COR_TEXTO_SECUNDARIO,
            font=("Segoe UI", 13, "bold")
        )

        self.titulo.grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(12, 0)
        )

        self.valor = ctk.CTkLabel(
            self,
            text=f"{valor:.0f}%",
            text_color=COR_TEXTO,
            font=("Consolas", 13, "bold")
        )

        self.valor.grid(
            row=0,
            column=1,
            sticky="e",
            padx=15,
            pady=(12, 0)
        )

        self.barra = ctk.CTkProgressBar(
            self,
            progress_color=cor,
            height=10
        )

        self.barra.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=(8, 15)
        )

        self.atualizar(valor)

    def atualizar(self, valor: float):

        valor = max(0, min(100, valor))

        self.valor.configure(
            text=f"{valor:.0f}%"
        )

        self.barra.set(
            valor / 100
        )