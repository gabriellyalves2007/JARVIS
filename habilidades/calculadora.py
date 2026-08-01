from habilidades.base import Habilidade

from assistente.comandos import abrir_calculadora


class Calculadora(Habilidade):

    def executar(
        self,
        comando: str = ""
    ) -> str:

        return abrir_calculadora()


calculadora = Calculadora()