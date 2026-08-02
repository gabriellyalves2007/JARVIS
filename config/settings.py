from pathlib import Path
from config.version import VERSION

class Settings:
    """
    Configurações globais do JARVIS.

    Toda configuração do projeto deverá
    ficar centralizada nesta classe.
    """

    APP_NAME = "JARVIS"

    DEBUG = True

    ROOT_DIR = Path(__file__).resolve().parent.parent

    DATA_DIR = ROOT_DIR / "dados"

    LOG_DIR = ROOT_DIR / "logs"

    TEST_DIR = ROOT_DIR / "tests"

    MEMORIA_FILE = DATA_DIR / "memoria.json"

    WORKSPACE_FILE = (
        DATA_DIR /
        "Jarvis.code-workspace"
    )

    GOOGLE_URL = "https://google.com"

    YOUTUBE_URL = "https://youtube.com"

    WIKIPEDIA_URL = (
        "https://pt.wikipedia.org/wiki/"
    )


settings = Settings()