from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Contexto:
    """
    Mantém o estado da conversa do JARVIS.
    """

    ultima_pergunta: str = ""
    ultima_resposta: str = ""
    ultima_intencao: Optional[object] = None

    historico: list = field(default_factory=list)

    limite_historico: int = 10

    def adicionar(
        self,
        pergunta: str,
        resposta: str,
        intencao=None
    ):
        """
        Adiciona uma nova interação ao contexto.
        """

        self.ultima_pergunta = pergunta
        self.ultima_resposta = resposta
        self.ultima_intencao = intencao

        self.historico.append(
            {
                "pergunta": pergunta,
                "resposta": resposta,
                "intencao": intencao,
            }
        )

        if len(self.historico) > self.limite_historico:
            self.historico.pop(0)

    def obter_historico(self):
        return self.historico.copy()

    def limpar(self):
        self.ultima_pergunta = ""
        self.ultima_resposta = ""
        self.ultima_intencao = None
        self.historico.clear()


contexto = Contexto()