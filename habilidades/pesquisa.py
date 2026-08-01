from habilidades.base import Habilidade

from assistente.comandos import pesquisar


class Pesquisa(Habilidade):

    def executar(
        self,
        comando: str = ""
    ) -> str:

        return pesquisar(comando)


pesquisa = Pesquisa()