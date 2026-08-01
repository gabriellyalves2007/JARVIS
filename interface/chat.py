import customtkinter as ctk


class ChatFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.configure(corner_radius=15)

        self.criar_componentes()

    def criar_componentes(self):
        titulo = ctk.CTkLabel(
            self,
            text="Conversa com Jarvis",
            font=("Segoe UI", 20, "bold")
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=10
        )

        self.caixa_chat = ctk.CTkTextbox(
            self,
            font=("Segoe UI", 15),
            corner_radius=10
        )

        self.caixa_chat.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=10
        )

        self.adicionar_mensagem(
            "Jarvis",
            "Olá, Gabrielly! Como posso ajudar?"
        )

    def adicionar_mensagem(self, autor: str, mensagem: str):
        self.caixa_chat.configure(state="normal")

        self.caixa_chat.insert(
            "end",
            f"{autor}: {mensagem}\n\n"
        )

        self.caixa_chat.configure(state="disabled")

        self.caixa_chat.see("end")