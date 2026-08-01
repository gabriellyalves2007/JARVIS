from core.intencoes import Intencao

from habilidades.google import google
from habilidades.youtube import youtube
from habilidades.calculadora import calculadora
from habilidades.horario import horario
from habilidades.memoria import Memoria
from habilidades.pesquisa import pesquisa


class RegistroHabilidades:

    def __init__(self):

        self._habilidades = {}

        self._registrar()

    def _registrar(self):

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
            Intencao.PESQUISAR,
            pesquisa
        )

    def registrar(
        self,
        intencao,
        habilidade
    ):
        self._habilidades[intencao] = habilidade

    def obter(
        self,
        intencao
    ):
        return self._habilidades.get(intencao)


registro = RegistroHabilidades()