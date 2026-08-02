"""
Controle de versão do JARVIS.
"""


MAJOR = 1
MINOR = 0
PATCH = 0

VERSION = (
    f"{MAJOR}."
    f"{MINOR}."
    f"{PATCH}"
)


def obter_versao() -> str:
    return VERSION