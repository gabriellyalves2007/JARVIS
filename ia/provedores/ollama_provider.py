from ia.provedores.base import ProvedorIA


class OllamaProvider(ProvedorIA):

    def responder(
        self,
        pergunta: str
    ) -> str:

        return (
            "Ollama ainda não configurado."
        )