from ia.provedores.base import ProvedorIA


class GeminiProvider(ProvedorIA):

    def responder(
        self,
        pergunta: str
    ) -> str:

        return (
            "Gemini ainda não configurado."
        )