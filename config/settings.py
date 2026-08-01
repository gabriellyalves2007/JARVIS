from dataclasses import dataclass


@dataclass
class Settings:
    """
    Configurações globais do JARVIS.
    """

    # ----------------------------
    # Inteligência Artificial
    # ----------------------------

    IA_PROVIDER: str = "openai"

    OPENAI_MODEL: str = "gpt-5"

    GEMINI_MODEL: str = "gemini-2.5-pro"

    OLLAMA_MODEL: str = "llama3.1"

    TEMPERATURE: float = 0.7

    TIMEOUT: int = 60

    # ----------------------------
    # Contexto
    # ----------------------------

    MAX_HISTORICO: int = 10

    # ----------------------------
    # Interface
    # ----------------------------

    TEMA: str = "dark"

    # ----------------------------
    # Debug
    # ----------------------------

    DEBUG: bool = True


settings = Settings()