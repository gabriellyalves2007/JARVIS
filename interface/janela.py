import customtkinter as ctk

from interface.header import Header
from interface.dashboard import Dashboard
from interface.chat import ChatFrame
from interface.footer import Footer
from interface.tema import COR_FUNDO


class JanelaJarvis(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("JARVIS AI")
        self.geometry("1400x850")
        self.minsize(1200, 700)

        self.configure(
            fg_color=COR_FUNDO
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Cabeçalho
        self.header = Header(self)

        # Área central
        self.centro = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.centro.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20,
            pady=10
        )

        self.centro.grid_columnconfigure(0, weight=2)
        self.centro.grid_columnconfigure(1, weight=3)
        self.centro.grid_rowconfigure(0, weight=1)

        # Dashboard
        self.dashboard = Dashboard(self.centro)

        self.dashboard.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        # Chat
        self.chat = ChatFrame(self.centro)

        self.chat.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        # Rodapé
        self.footer = Footer(
            self,
            self.chat,
            self.dashboard
        )

        self.footer.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(10, 20)
        )