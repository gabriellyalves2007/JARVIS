from enum import Enum, auto


class EstadoJarvis(Enum):
    EM_ESPERA = auto()
    ESCUTANDO = auto()
    PROCESSANDO = auto()
    EXECUTANDO = auto()
    SUCESSO = auto()
    ERRO = auto()


class Humor:
    """
    Armazena o estado operacional atual do assistente.
    """

    def __init__(self):
        self.estado = EstadoJarvis.EM_ESPERA

    def alterar(self, novo_estado: EstadoJarvis) -> None:
        self.estado = novo_estado

    def obter(self) -> EstadoJarvis:
        return self.estado


humor = Humor()