from ia.provedores.base import ProvedorIA


class OpenAIProvider(ProvedorIA):

    def responder(
        self,
        pergunta: str
    ) -> str:

        return (
            "OpenAI ainda não configurado."
        )