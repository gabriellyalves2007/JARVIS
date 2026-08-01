from core.contexto import contexto
from core.intencoes import Intencao

from habilidades.registro import registro


def executar_intencao(
    intencao: Intencao,
    comando: str
) -> str:
    """
    Executa uma intenção utilizando o registro de habilidades.
    """

    habilidade = registro.obter(intencao)

    if habilidade:
        return habilidade.executar(comando)

    if intencao == Intencao.REPETIR:

        if contexto.ultima_resposta:
            return contexto.ultima_resposta

        return "Ainda não tenho nenhuma resposta para repetir."

    return "Ainda não existe uma habilidade para essa intenção."