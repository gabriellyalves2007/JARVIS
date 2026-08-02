from dataclasses import dataclass
from typing import Optional

import win32con
import win32gui


@dataclass
class Janela:
    """
    Representa uma janela visível do Windows.
    """

    handle: int
    titulo: str


class GerenciadorJanelas:
    """
    Localiza e controla janelas abertas no Windows.
    """

    @staticmethod
    def _janela_valida(handle: int) -> bool:
        if not win32gui.IsWindowVisible(handle):
            return False

        titulo = win32gui.GetWindowText(handle).strip()

        return bool(titulo)

    def listar(self) -> list[Janela]:
        """
        Retorna todas as janelas visíveis que possuem título.
        """

        janelas: list[Janela] = []

        def adicionar(handle: int, _parametro) -> None:
            if not self._janela_valida(handle):
                return

            titulo = win32gui.GetWindowText(handle).strip()

            janelas.append(
                Janela(
                    handle=handle,
                    titulo=titulo,
                )
            )

        win32gui.EnumWindows(adicionar, None)

        return sorted(
            janelas,
            key=lambda janela: janela.titulo.lower(),
        )

    def localizar(self, nome: str) -> Optional[Janela]:
        """
        Procura uma janela por parte do título.

        Exemplos:
            localizar("chrome")
            localizar("spotify")
            localizar("visual studio code")
        """

        nome = str(nome).strip().lower()

        if not nome:
            return None

        for janela in self.listar():
            if nome in janela.titulo.lower():
                return janela

        return None

    def janela_ativa(self) -> Optional[Janela]:
        """
        Retorna a janela que está em primeiro plano.
        """

        handle = win32gui.GetForegroundWindow()

        if not handle:
            return None

        titulo = win32gui.GetWindowText(handle).strip()

        if not titulo:
            return None

        return Janela(
            handle=handle,
            titulo=titulo,
        )

    def minimizar(self, nome: str) -> bool:
        janela = self.localizar(nome)

        if janela is None:
            return False

        try:
            win32gui.ShowWindow(
                janela.handle,
                win32con.SW_MINIMIZE,
            )

            return True

        except Exception as erro:
            print(
                f"Erro ao minimizar '{nome}': {erro}"
            )

            return False

    def maximizar(self, nome: str) -> bool:
        janela = self.localizar(nome)

        if janela is None:
            return False

        try:
            win32gui.ShowWindow(
                janela.handle,
                win32con.SW_MAXIMIZE,
            )

            return True

        except Exception as erro:
            print(
                f"Erro ao maximizar '{nome}': {erro}"
            )

            return False

    def restaurar(self, nome: str) -> bool:
        janela = self.localizar(nome)

        if janela is None:
            return False

        try:
            win32gui.ShowWindow(
                janela.handle,
                win32con.SW_RESTORE,
            )

            return True

        except Exception as erro:
            print(
                f"Erro ao restaurar '{nome}': {erro}"
            )

            return False

    def focar(self, nome: str) -> bool:
        """
        Restaura e traz a janela para frente.
        """

        janela = self.localizar(nome)

        if janela is None:
            return False

        try:
            if win32gui.IsIconic(janela.handle):
                win32gui.ShowWindow(
                    janela.handle,
                    win32con.SW_RESTORE,
                )

            win32gui.SetForegroundWindow(
                janela.handle
            )

            return True

        except Exception as erro:
            print(
                f"Erro ao focar '{nome}': {erro}"
            )

            return False


janelas = GerenciadorJanelas()