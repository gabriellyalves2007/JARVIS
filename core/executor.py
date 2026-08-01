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
    Executa todas as etapas do plano em ordem
    e registra o estado de cada uma.
    """

    etapas = plano.get("etapas", [])

    if not etapas:
        return "Não encontrei nenhuma ação para executar."

    respostas = []

    for etapa in etapas:
        intencao = etapa.get("intencao")
        comando = etapa.get("comando", "")

        etapa["executado"] = False
        etapa["resposta"] = ""
        etapa["erro"] = ""

        if intencao is None:
            etapa["erro"] = (
                "Não consegui identificar a intenção."
            )

            respostas.append(etapa["erro"])
            continue

        try:
            resposta = executar_intencao(
                intencao=intencao,
                comando=comando
            )

            etapa["resposta"] = resposta
            etapa["executado"] = True

            if resposta:
                respostas.append(resposta)

        except Exception as erro:
            mensagem_erro = (
                f"Não consegui executar a etapa "
                f"{etapa.get('numero', '?')}."
            )

            etapa["erro"] = str(erro)
            etapa["executado"] = False

            print(
                f"❌ Erro na etapa "
                f"{etapa.get('numero', '?')}: {erro}"
            )

            respostas.append(mensagem_erro)

    if not respostas:
        return "Não consegui executar o plano."

    return "\n".join(respostas)