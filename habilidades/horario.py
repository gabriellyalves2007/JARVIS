from habilidades.base import Habilidade

from assistente.comandos import informar_horas


class Horario(Habilidade):

    def executar(
        self,
        comando: str = ""
    ) -> str:

        return informar_horas()


horario = Horario()