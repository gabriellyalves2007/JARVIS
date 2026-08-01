from enum import Enum

from core.intencoes import Intencao
from ia.interpretador import interpretador


class Destino(Enum):
    EXECUTOR = "executor"
    MEMORIA = "memoria"
    IA = "ia"
    INTERNET = "internet"
    PLUGIN = "plugin"
    DESCONHECIDO = "desconhecido"


class Router:
    """
    Decide qual componente deve processar
    o comando recebido pelo JARVIS.
    """

    def decidir(
        self,
        intencao: Intencao,
        comando: str
    ) -> Destino:
        if intencao is None:
            return Destino.DESCONHECIDO

        texto = interpretador.interpretar(
            comando
        )

        perguntas_conhecimento = (
            "quem e",
            "quem foi",
            "o que e",
            "o que sao",
            "explique",
            "fale sobre",
            "me explique",
            "defina",
        )

        if (
            intencao == Intencao.PESQUISAR
            and any(
                expressao in texto
                for expressao in perguntas_conhecimento
            )
        ):
            return Destino.INTERNET

        pesquisas_google = (
            "pesquise",
            "pesquisar",
            "procure",
            "buscar",
            "busque",
        )

        if (
            intencao == Intencao.PESQUISAR
            and any(
                expressao in texto
                for expressao in pesquisas_google
            )
        ):
            return Destino.EXECUTOR

        intencoes_executor = {
            Intencao.ABRIR_GOOGLE,
            Intencao.ABRIR_YOUTUBE,
            Intencao.ABRIR_CALCULADORA,
            Intencao.INFORMAR_HORAS,
            Intencao.SALVAR_NOME,
            Intencao.LEMBRAR_NOME,
            Intencao.REPETIR,
            Intencao.CONSULTAR_TAREFA,
            Intencao.PESQUISAR,
        }

        if intencao in intencoes_executor:
            return Destino.EXECUTOR

        return Destino.DESCONHECIDO


router = Router()