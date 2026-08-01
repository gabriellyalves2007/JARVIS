import threading

import customtkinter as ctk

from assistente.voz import ouvir
from core.core import processar_entrada

from ia.humor import EstadoJarvis, humor

from interface.tema import (
    COR_PAINEL,
    COR_PAINEL_CLARO,
    COR_CIANO,
    COR_VERDE,
    COR_TEXTO,
    COR_TEXTO_SECUNDARIO,
)


COR_ERRO = "#FF4D4D"


class Footer(ctk.CTkFrame):

    def __init__(self, master, chat, dashboard):
        super().__init__(
            master,
            fg_color=COR_PAINEL,
            corner_radius=15
        )

        self.chat = chat
        self.dashboard = dashboard

        self.processando = False
        self.escutando = False

        self.grid_columnconfigure(0, weight=1)

        self.criar_componentes()

    def criar_componentes(self):
        self.entrada = ctk.CTkEntry(
            self,
            placeholder_text="Como posso ajudar?",
            height=48,
            corner_radius=12,
            fg_color=COR_PAINEL_CLARO,
            border_color=COR_CIANO,
            border_width=1,
            text_color=COR_TEXTO,
            placeholder_text_color=COR_TEXTO_SECUNDARIO,
            font=("Segoe UI", 14)
        )

        self.entrada.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(15, 10),
            pady=15
        )

        self.btn_microfone = ctk.CTkButton(
            self,
            text="🎤",
            width=48,
            height=48,
            corner_radius=12,
            fg_color=COR_PAINEL_CLARO,
            hover_color="#18334A",
            border_width=1,
            border_color=COR_CIANO,
            font=("Segoe UI Emoji", 18),
            command=self.iniciar_escuta
        )

        self.btn_microfone.grid(
            row=0,
            column=1,
            padx=(0, 10),
            pady=15
        )

        self.btn_enviar = ctk.CTkButton(
            self,
            text="➜",
            width=48,
            height=48,
            corner_radius=12,
            fg_color=COR_CIANO,
            hover_color="#00B8D9",
            text_color="#050B14",
            font=("Segoe UI", 20, "bold"),
            command=self.iniciar_processamento
        )

        self.btn_enviar.grid(
            row=0,
            column=2,
            padx=(0, 15),
            pady=15
        )

        self.entrada.bind(
            "<Return>",
            self.enviar_com_enter
        )

        self.entrada.focus()

    def enviar_com_enter(self, _event):
        self.iniciar_processamento()

    def iniciar_processamento(self):
        texto = self.entrada.get().strip()

        if not texto or self.processando:
            return

        self.processando = True

        self.entrada.delete(0, "end")

        self.chat.adicionar_mensagem(
            "Você",
            texto
        )

        self.alterar_estado(
            estado=EstadoJarvis.PROCESSANDO,
            texto_estado="PROCESSANDO",
            ultima_acao="Analisando comando",
            cor=COR_CIANO
        )

        self.bloquear_controles()

        thread = threading.Thread(
            target=self.processar_em_segundo_plano,
            args=(texto,),
            daemon=True
        )

        thread.start()

    def processar_em_segundo_plano(self, texto: str):
        try:
            humor.alterar(
                EstadoJarvis.EXECUTANDO
            )

            resposta = processar_entrada(texto)

            self.after(
                0,
                lambda: self.finalizar_processamento(
                    resposta=resposta,
                    ocorreu_erro=False
                )
            )

        except Exception as erro:
            print(
                f"Erro ao processar mensagem: {erro}"
            )

            self.after(
                0,
                lambda: self.finalizar_processamento(
                    resposta=(
                        "Não consegui processar "
                        "essa solicitação."
                    ),
                    ocorreu_erro=True
                )
            )

    def finalizar_processamento(
        self,
        resposta: str,
        ocorreu_erro: bool
    ):
        self.chat.adicionar_mensagem(
            "Jarvis",
            resposta
        )

        resumo_resposta = self.resumir_texto(
            resposta,
            limite=35
        )

        if ocorreu_erro:
            self.alterar_estado(
                estado=EstadoJarvis.ERRO,
                texto_estado="ERRO",
                ultima_acao=resumo_resposta,
                cor=COR_ERRO
            )
        else:
            self.alterar_estado(
                estado=EstadoJarvis.SUCESSO,
                texto_estado="CONCLUÍDO",
                ultima_acao=resumo_resposta,
                cor=COR_VERDE
            )

        self.processando = False
        self.desbloquear_controles()
        self.entrada.focus()

        self.after(
            1200,
            self.voltar_para_espera
        )

    def voltar_para_espera(self):
        if self.processando or self.escutando:
            return

        self.alterar_estado(
            estado=EstadoJarvis.EM_ESPERA,
            texto_estado="EM ESPERA",
            ultima_acao=(
                self.dashboard
                .core_widget
                .ultima_acao_card
                .label_valor
                .cget("text")
            ),
            cor=COR_CIANO
        )

    def iniciar_escuta(self):
        if self.escutando or self.processando:
            return

        self.escutando = True

        self.btn_microfone.configure(
            text="●",
            state="disabled"
        )

        self.btn_enviar.configure(
            state="disabled"
        )

        self.dashboard.microfone_card.atualizar(
            status="ESCUTANDO",
            cor=COR_VERDE
        )

        self.alterar_estado(
            estado=EstadoJarvis.ESCUTANDO,
            texto_estado="ESCUTANDO",
            ultima_acao="Aguardando voz",
            cor=COR_VERDE
        )

        thread = threading.Thread(
            target=self.ouvir_em_segundo_plano,
            daemon=True
        )

        thread.start()

    def ouvir_em_segundo_plano(self):
        texto = ouvir()

        self.after(
            0,
            lambda: self.finalizar_escuta(texto)
        )

    def finalizar_escuta(self, texto: str):
        self.escutando = False

        self.btn_microfone.configure(
            text="🎤",
            state="normal"
        )

        self.btn_enviar.configure(
            state="normal"
        )

        self.dashboard.microfone_card.atualizar(
            status="EM ESPERA",
            cor=COR_TEXTO_SECUNDARIO
        )

        if not texto:
            self.alterar_estado(
                estado=EstadoJarvis.EM_ESPERA,
                texto_estado="EM ESPERA",
                ultima_acao="Nenhuma fala detectada",
                cor=COR_CIANO
            )

            self.entrada.focus()
            return

        self.entrada.delete(0, "end")
        self.entrada.insert(0, texto)

        self.iniciar_processamento()

    def alterar_estado(
        self,
        estado: EstadoJarvis,
        texto_estado: str,
        ultima_acao: str,
        cor: str
    ):
        humor.alterar(estado)

        self.dashboard.core_widget.alterar_estado(
            estado=texto_estado,
            mensagem=ultima_acao,
            cor=cor
        )

    def bloquear_controles(self):
        self.entrada.configure(
            state="disabled"
        )

        self.btn_enviar.configure(
            state="disabled"
        )

        self.btn_microfone.configure(
            state="disabled"
        )

    def desbloquear_controles(self):
        self.entrada.configure(
            state="normal"
        )

        self.btn_enviar.configure(
            state="normal"
        )

        self.btn_microfone.configure(
            state="normal"
        )

    @staticmethod
    def resumir_texto(
        texto: str,
        limite: int
    ) -> str:
        texto = str(texto).strip()

        if len(texto) <= limite:
            return texto

        return texto[:limite].rstrip() + "..."