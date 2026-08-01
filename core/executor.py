from core.contexto import contexto
from core.intencoes import Intencao

from habilidades.registro import registro


def executar_intencao(
    intencao: Intencao,
    comando: str
) -> str:
    """
    Executa uma única intenção utilizando
    o registro de habilidades.
    """

    if intencao == Intencao.REPETIR:
        if contexto.ultima_resposta:
            return contexto.ultima_resposta

        return "Ainda não tenho nenhuma resposta para repetir."

    habilidade = registro.obter(intencao)

    if habilidade is None:
        return (
            "Ainda não existe uma habilidade "
            "para essa intenção."
        )

    resposta = habilidade.executar(comando)

    if resposta is None:
        return "A ação foi executada sem uma resposta."

    return str(resposta).strip()


def executar_plano(plano: dict) -> str:
    """
    Executa todas as etapas de um plano na ordem.
    """

    etapas = plano.get("etapas", [])

    if not etapas:
        return "Não encontrei nenhuma ação para executar."

    respostas = []

    for etapa in etapas:
        intencao = etapa.get("intencao")
        comando = etapa.get("comando", "")

        if intencao is None:
            respostas.append(
                "Não consegui identificar uma das ações."
            )
            continue

        resposta = executar_intencao(
            intencao=intencao,
            comando=comando
        )

        if resposta:
            respostas.append(resposta)

    if not respostas:
        return "Não consegui executar o plano."

    return "\n".join(respostas)