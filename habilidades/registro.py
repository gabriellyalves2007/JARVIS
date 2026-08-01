from core.intencoes import Intencao

from habilidades.calculadora import calculadora
from habilidades.google import google
from habilidades.horario import horario
from habilidades.memoria import Memoria
from habilidades.pesquisa import pesquisa
from habilidades.programa import programa
from habilidades.tarefa import HabilidadeTarefa
from habilidades.youtube import youtube


class RegistroHabilidades:
    """
    Registra e localiza as habilidades
    disponíveis no JARVIS.
    """

    def __init__(self):
        self._habilidades = {}

        self._registrar()

    def _registrar(self) -> None:
        self.registrar(
            Intencao.ABRIR_GOOGLE,
            google
        )

        self.registrar(
            Intencao.ABRIR_YOUTUBE,
            youtube
        )

        self.registrar(
            Intencao.ABRIR_CALCULADORA,
            calculadora
        )

        self.registrar(
            Intencao.ABRIR_PROGRAMA,
            programa
        )

        self.registrar(
            Intencao.INFORMAR_HORAS,
            horario
        )

        self.registrar(
            Intencao.SALVAR_NOME,
            Memoria(
                Intencao.SALVAR_NOME
            )
        )

        self.registrar(
            Intencao.LEMBRAR_NOME,
            Memoria(
                Intencao.LEMBRAR_NOME
            )
        )

        self.registrar(
            Intencao.CONSULTAR_TAREFA,
            HabilidadeTarefa(
                Intencao.CONSULTAR_TAREFA
            )
        )

        self.registrar(
            Intencao.CANCELAR_TAREFA,
            HabilidadeTarefa(
                Intencao.CANCELAR_TAREFA
            )
        )

        self.registrar(
            Intencao.PESQUISAR,
            pesquisa
        )

    def registrar(
        self,
        intencao: Intencao,
        habilidade
    ) -> None:
        self._habilidades[
            intencao
        ] = habilidade

    def obter(
        self,
        intencao: Intencao
    ):
        return self._habilidades.get(
            intencao
        )

    def existe(
        self,
        intencao: Intencao
    ) -> bool:
        return intencao in self._habilidades

    def listar(self) -> list:
        return list(
            self._habilidades.keys()
        )


registro = RegistroHabilidades()