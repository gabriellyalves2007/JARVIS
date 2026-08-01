from enum import Enum

from core.intencoes import Intencao


class Destino(Enum):
    """
    Destinos possíveis para o processamento
    de um comando do JARVIS.
    """

    EXECUTOR = "executor"
    MEMORIA = "memoria"
    IA = "ia"
    INTERNET = "internet"
    PLUGIN = "plugin"
    DESCONHECIDO = "desconhecido"


class Router:
    """
    Decide qual componente deve processar
    uma intenção identificada pelo JARVIS.
    """

    def decidir(
        self,
        intencao: Intencao,
        comando: str
    ) -> Destino:
        if intencao is None:
            return Destino.DESCONHECIDO

        intencoes_executor = {
            Intencao.ABRIR_GOOGLE,
            Intencao.ABRIR_YOUTUBE,
            Intencao.ABRIR_CALCULADORA,
            Intencao.INFORMAR_HORAS,
            Intencao.SALVAR_NOME,
            Intencao.LEMBRAR_NOME,
            Intencao.REPETIR,
            Intencao.PESQUISAR,
        }

        if intencao in intencoes_executor:
            return Destino.EXECUTOR

        return Destino.DESCONHECIDO


router = Router()