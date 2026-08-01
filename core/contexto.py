from datetime import datetime


class ContextoConversa:

    def __init__(self):
        self.limpar()

    def atualizar(
        self,
        intencao,
        comando: str,
        resposta: str
    ):
        self.ultima_intencao = intencao
        self.ultimo_comando = comando
        self.ultima_resposta = resposta
        self.ultimo_horario = datetime.now()

    def limpar(self):
        self.ultima_intencao = None
        self.ultimo_comando = ""
        self.ultima_resposta = ""
        self.ultimo_horario = None

    def existe_contexto(self) -> bool:
        return self.ultima_intencao is not None


contexto = ContextoConversa()