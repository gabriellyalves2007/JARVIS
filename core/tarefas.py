from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EtapaTarefa:
    """
    Representa uma etapa individual de uma tarefa.
    """

    numero: int
    comando: str

    concluida: bool = False
    resposta: str = ""
    erro: str = ""


@dataclass
class Tarefa:
    """
    Representa uma tarefa completa executada pelo JARVIS.
    """

    nome: str
    total_etapas: int

    etapa_atual: int = 0
    concluida: bool = False
    cancelada: bool = False

    etapas: list[EtapaTarefa] = field(
        default_factory=list
    )


class GerenciadorTarefas:
    """
    Acompanha a tarefa atual e o progresso
    de suas etapas.
    """

    def __init__(self):
        self._tarefa: Optional[Tarefa] = None

    def iniciar(self, plano: dict) -> None:
        """
        Cria uma nova tarefa a partir do plano.
        """

        etapas_plano = plano.get(
            "etapas",
            []
        )

        etapas = []

        for etapa in etapas_plano:
            etapas.append(
                EtapaTarefa(
                    numero=etapa.get(
                        "numero",
                        len(etapas) + 1
                    ),
                    comando=etapa.get(
                        "comando",
                        ""
                    )
                )
            )

        self._tarefa = Tarefa(
            nome=plano.get(
                "comando_original",
                "Tarefa do JARVIS"
            ),
            total_etapas=len(etapas),
            etapas=etapas
        )

    def marcar_concluida(
        self,
        numero: int,
        resposta: str = ""
    ) -> None:
        """
        Marca uma etapa específica como concluída.
        """

        tarefa = self._tarefa

        if tarefa is None:
            return

        etapa = self._localizar_etapa(numero)

        if etapa is None:
            return

        etapa.concluida = True
        etapa.resposta = str(resposta).strip()
        etapa.erro = ""

        tarefa.etapa_atual = numero

        if all(
            item.concluida
            for item in tarefa.etapas
        ):
            tarefa.concluida = True

    def marcar_erro(
        self,
        numero: int,
        mensagem: str
    ) -> None:
        """
        Registra um erro ocorrido em uma etapa.
        """

        tarefa = self._tarefa

        if tarefa is None:
            return

        etapa = self._localizar_etapa(numero)

        if etapa is None:
            return

        etapa.concluida = False
        etapa.erro = str(mensagem).strip()

        tarefa.etapa_atual = numero
        tarefa.concluida = False

    def cancelar(self) -> tuple[bool, str]:
        """
        Solicita o cancelamento da tarefa atual.

        O cancelamento será respeitado antes
        da próxima etapa começar.
        """

        tarefa = self._tarefa

        if tarefa is None:
            return (
                False,
                "Não existe nenhuma tarefa para cancelar."
            )

        if tarefa.cancelada:
            return (
                False,
                "A tarefa atual já foi cancelada."
            )

        if tarefa.concluida:
            return (
                False,
                "A última tarefa já foi concluída."
            )

        tarefa.cancelada = True

        return (
            True,
            "Cancelamento solicitado. "
            "As próximas etapas não serão executadas."
        )

    def foi_cancelada(self) -> bool:
        """
        Informa se a tarefa atual foi cancelada.
        """

        return bool(
            self._tarefa
            and self._tarefa.cancelada
        )

    def obter(self) -> Optional[Tarefa]:
        """
        Retorna a tarefa atual.
        """

        return self._tarefa

    def obter_progresso(self) -> str:
        """
        Retorna o progresso em formato de texto.
        """

        tarefa = self._tarefa

        if tarefa is None:
            return "Nenhuma tarefa em andamento."

        concluidas = sum(
            1
            for etapa in tarefa.etapas
            if etapa.concluida
        )

        if tarefa.cancelada:
            return (
                "A tarefa atual foi cancelada após "
                f"{concluidas} de "
                f"{tarefa.total_etapas} etapas."
            )

        if tarefa.concluida:
            return (
                "Tarefa concluída: "
                f"{tarefa.total_etapas} de "
                f"{tarefa.total_etapas} etapas."
            )

        return (
            f"Progresso: {concluidas} de "
            f"{tarefa.total_etapas} etapas."
        )

    def limpar(self) -> None:
        """
        Remove a tarefa atual.
        """

        self._tarefa = None

    def _localizar_etapa(
        self,
        numero: int
    ) -> Optional[EtapaTarefa]:
        tarefa = self._tarefa

        if tarefa is None:
            return None

        for etapa in tarefa.etapas:
            if etapa.numero == numero:
                return etapa

        return None


gerenciador_tarefas = GerenciadorTarefas()