from core.contexto import contexto
from core.intencoes import Intencao

from habilidades.registro import registro


def executar_intencao(
    intencao: Intencao,
    comando: str
) -> str:
    """
    Executa uma única intenção usando
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
    Executa todas as etapas do plano em ordem.

    Se ocorrer uma falha real durante uma etapa,
    interrompe as próximas ações para evitar
    uma execução inconsistente.
    """

    etapas = plano.get("etapas", [])

    if not etapas:
        return "Não encontrei nenhuma ação para executar."

    respostas = []

    for etapa in etapas:
        numero = etapa.get("numero", "?")
        intencao = etapa.get("intencao")
        comando = etapa.get("comando", "")

        etapa["executado"] = False
        etapa["resposta"] = ""
        etapa["erro"] = ""

        if intencao is None:
            mensagem = (
                f"Não consegui identificar a etapa {numero}. "
                "As próximas ações foram canceladas."
            )

            etapa["erro"] = mensagem
            respostas.append(mensagem)

            print(
                f"❌ Etapa {numero} sem intenção identificada."
            )

            break

        try:
            print(
                f"⚙️ Executando etapa {numero}: "
                f"{intencao.name} → {comando}"
            )

            resposta = executar_intencao(
                intencao=intencao,
                comando=comando
            )

            resposta = str(resposta).strip()

            etapa["resposta"] = resposta
            etapa["executado"] = True

            if resposta:
                respostas.append(resposta)

            print(
                f"✅ Etapa {numero} concluída."
            )

        except Exception as erro:
            mensagem = (
                f"Não consegui executar a etapa {numero}. "
                "As próximas ações foram canceladas."
            )

            etapa["erro"] = str(erro)
            etapa["executado"] = False

            print(
                f"❌ Erro na etapa {numero}: {erro}"
            )

            respostas.append(mensagem)

            break

    if not respostas:
        return "Não consegui executar o plano."

    return "\n".join(respostas)