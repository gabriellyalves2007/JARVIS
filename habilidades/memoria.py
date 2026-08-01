from habilidades.base import Habilidade

from assistente.comandos import (
    salvar_nome,
    lembrar_nome,
)

from core.intencoes import Intencao


class Memoria(Habilidade):

    def __init__(
        self,
        intencao
    ):
        self.intencao = intencao

    def executar(
        self,
        comando: str = ""
    ) -> str:

        if self.intencao == Intencao.SALVAR_NOME:
            return salvar_nome(comando)

        return lembrar_nome()