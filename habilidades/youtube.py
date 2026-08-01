from habilidades.base import Habilidade

from assistente.comandos import abrir_youtube


class Youtube(Habilidade):

    def executar(
        self,
        comando: str = ""
    ) -> str:

        return abrir_youtube()


youtube = Youtube()