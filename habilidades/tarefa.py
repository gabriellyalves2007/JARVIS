from core.intencoes import Intencao
from core.tarefas import gerenciador_tarefas

from habilidades.base import Habilidade


class HabilidadeTarefa(Habilidade):
    """
    Consulta ou cancela a tarefa atual.
    """

    def __init__(
        self,
        intencao: Intencao
    ):
        self.intencao = intencao

    def executar(
        self,
        comando: str = ""
    ) -> str:
        if (
            self.intencao
            == Intencao.CANCELAR_TAREFA
        ):
            return self._cancelar()

        return self._consultar()

    @staticmethod
    def _cancelar() -> str:
        sucesso, mensagem = (
            gerenciador_tarefas.cancelar()
        )

        if sucesso:
            print("⛔ Cancelamento solicitado.")

        return mensagem

    @staticmethod
    def _consultar() -> str:
        tarefa = gerenciador_tarefas.obter()

        if tarefa is None:
            return (
                "Nenhuma tarefa foi executada ainda."
            )

        etapas_concluidas = sum(
            1
            for etapa in tarefa.etapas
            if etapa.concluida
        )

        if tarefa.cancelada:
            return (
                f"A tarefa '{tarefa.nome}' "
                "foi cancelada. "
                f"Foram concluídas "
                f"{etapas_concluidas} de "
                f"{tarefa.total_etapas} etapas."
            )

        etapas_com_erro = [
            etapa
            for etapa in tarefa.etapas
            if etapa.erro
        ]

        if etapas_com_erro:
            etapa_erro = etapas_com_erro[0]

            return (
                f"A tarefa '{tarefa.nome}' "
                f"parou na etapa "
                f"{etapa_erro.numero}. "
                f"Foram concluídas "
                f"{etapas_concluidas} de "
                f"{tarefa.total_etapas} etapas."
            )

        if tarefa.concluida:
            return (
                f"A tarefa '{tarefa.nome}' "
                "foi concluída. "
                f"Foram executadas "
                f"{tarefa.total_etapas} etapas."
            )

        proxima_etapa = (
            HabilidadeTarefa
            ._obter_proxima_etapa(tarefa)
        )

        resposta = (
            f"A tarefa atual é '{tarefa.nome}'. "
            f"O progresso está em "
            f"{etapas_concluidas} de "
            f"{tarefa.total_etapas} etapas."
        )

        if proxima_etapa is not None:
            resposta += (
                " A próxima etapa é: "
                f"'{proxima_etapa.comando}'."
            )

        return resposta

    @staticmethod
    def _obter_proxima_etapa(tarefa):
        for etapa in tarefa.etapas:
            if (
                not etapa.concluida
                and not etapa.erro
            ):
                return etapa

        return None