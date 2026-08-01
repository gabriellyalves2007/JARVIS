from core.contexto import contexto
from core.intencoes import Intencao
from core.tarefas import gerenciador_tarefas

from habilidades.registro import registro


INTENCOES_CONTROLE_TAREFA = {
    Intencao.CONSULTAR_TAREFA,
    Intencao.CANCELAR_TAREFA,
}


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

        return (
            "Ainda não tenho nenhuma resposta "
            "para repetir."
        )

    habilidade = registro.obter(
        intencao
    )

    if habilidade is None:
        return (
            "Ainda não existe uma habilidade "
            "para essa intenção."
        )

    resposta = habilidade.executar(
        comando
    )

    if resposta is None:
        return (
            "A ação foi executada sem uma resposta."
        )

    return str(resposta).strip()


def executar_plano(
    plano: dict
) -> str:
    """
    Executa as etapas do plano em ordem.

    Consultas e cancelamentos não substituem
    a tarefa que já está registrada.
    """

    etapas = plano.get(
        "etapas",
        []
    )

    if not etapas:
        return (
            "Não encontrei nenhuma ação "
            "para executar."
        )

    apenas_controle_tarefa = (
        len(etapas) == 1
        and etapas[0].get("intencao")
        in INTENCOES_CONTROLE_TAREFA
    )

    if not apenas_controle_tarefa:
        gerenciador_tarefas.iniciar(
            plano
        )

    respostas = []

    for etapa in etapas:
        numero = etapa.get(
            "numero",
            "?"
        )

        intencao = etapa.get(
            "intencao"
        )

        comando = etapa.get(
            "comando",
            ""
        )

        etapa["executado"] = False
        etapa["resposta"] = ""
        etapa["erro"] = ""

        if (
            not apenas_controle_tarefa
            and gerenciador_tarefas.foi_cancelada()
        ):
            mensagem = (
                "A tarefa foi cancelada. "
                "As próximas ações não serão executadas."
            )

            respostas.append(
                mensagem
            )

            print(
                "⛔ Execução cancelada."
            )

            break

        if intencao is None:
            mensagem = (
                f"Não consegui identificar "
                f"a etapa {numero}. "
                "As próximas ações foram canceladas."
            )

            etapa["erro"] = mensagem

            if (
                not apenas_controle_tarefa
                and isinstance(numero, int)
            ):
                gerenciador_tarefas.marcar_erro(
                    numero=numero,
                    mensagem=mensagem
                )

            respostas.append(
                mensagem
            )

            print(
                f"❌ Etapa {numero} sem intenção."
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

            resposta = str(
                resposta
            ).strip()

            etapa["resposta"] = resposta
            etapa["executado"] = True

            if (
                not apenas_controle_tarefa
                and isinstance(numero, int)
            ):
                gerenciador_tarefas.marcar_concluida(
                    numero=numero,
                    resposta=resposta
                )

            if resposta:
                respostas.append(
                    resposta
                )

            print(
                f"✅ Etapa {numero} concluída."
            )

            if not apenas_controle_tarefa:
                print(
                    "📊 "
                    f"{gerenciador_tarefas.obter_progresso()}"
                )

        except Exception as erro:
            mensagem = (
                f"Não consegui executar "
                f"a etapa {numero}. "
                "As próximas ações foram canceladas."
            )

            etapa["erro"] = str(
                erro
            )

            etapa["executado"] = False

            if (
                not apenas_controle_tarefa
                and isinstance(numero, int)
            ):
                gerenciador_tarefas.marcar_erro(
                    numero=numero,
                    mensagem=str(erro)
                )

            print(
                f"❌ Erro na etapa {numero}: "
                f"{erro}"
            )

            respostas.append(
                mensagem
            )

            break

    if not respostas:
        return (
            "Não consegui executar o plano."
        )

    return "\n".join(
        respostas
    )