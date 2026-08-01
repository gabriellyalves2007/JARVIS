from config import settings

from ia.provedores.gemini_provider import GeminiProvider
from ia.provedores.ollama_provider import OllamaProvider
from ia.provedores.openai_provider import OpenAIProvider


class FabricaIA:
    """
    Retorna o provedor de IA configurado.
    """

    @staticmethod
    def obter():

        provider = settings.IA_PROVIDER.lower()

        if provider == "openai":
            return OpenAIProvider()

        if provider == "gemini":
            return GeminiProvider()

        if provider == "ollama":
            return OllamaProvider()

        return OpenAIProvider()