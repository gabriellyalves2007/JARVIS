from habilidades.base import Habilidade

from assistente.comandos import abrir_google


class Google(Habilidade):

    def executar(
        self,
        comando: str = ""
    ) -> str:

        return abrir_google()


google = Google()