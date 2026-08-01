from abc import ABC, abstractmethod


class ProvedorIA(ABC):
    """
    Interface base para qualquer provedor de IA.
    """

    @abstractmethod
    def responder(
        self,
        pergunta: str
    ) -> str:
        """
        Retorna uma resposta para a pergunta.
        """
        raise NotImplementedError