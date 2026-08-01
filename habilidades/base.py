from abc import ABC, abstractmethod


class Habilidade(ABC):
    """
    Classe base de todas as habilidades do JARVIS.
    """

    @abstractmethod
    def executar(
        self,
        comando: str = ""
    ) -> str:
        pass