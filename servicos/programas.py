import os
import subprocess
from pathlib import Path
from typing import Optional


class GerenciadorProgramas:
    """
    Localiza e abre programas instalados no Windows.

    Cada programa pode possuir:
    - um nome principal;
    - vários apelidos;
    - vários caminhos possíveis.
    """

    def __init__(self):
        self.programas = {
            "chrome": {
                "apelidos": (
                    "chrome",
                    "google chrome",
                    "navegador chrome",
                ),
                "caminhos": (
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                    r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe",
                ),
            },

            "edge": {
                "apelidos": (
                    "edge",
                    "microsoft edge",
                    "navegador edge",
                ),
                "caminhos": (
                    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                    r"%PROGRAMFILES(X86)%\Microsoft\Edge\Application\msedge.exe",
                ),
            },

            "firefox": {
                "apelidos": (
                    "firefox",
                    "mozilla firefox",
                    "mozilla",
                ),
                "caminhos": (
                    r"C:\Program Files\Mozilla Firefox\firefox.exe",
                    r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
                ),
            },

            "vscode": {
                "apelidos": (
                    "vscode",
                    "vs code",
                    "visual studio code",
                    "code",
                ),
                "caminhos": (
                    r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe",
                    r"C:\Program Files\Microsoft VS Code\Code.exe",
                    r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
                ),
            },

            "spotify": {
                "apelidos": (
                    "spotify",
                ),
                "caminhos": (
                    r"%APPDATA%\Spotify\Spotify.exe",
                    r"%LOCALAPPDATA%\Microsoft\WindowsApps\Spotify.exe",
                ),
            },

            "word": {
                "apelidos": (
                    "word",
                    "microsoft word",
                ),
                "caminhos": (
                    r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE",
                ),
            },

            "excel": {
                "apelidos": (
                    "excel",
                    "microsoft excel",
                ),
                "caminhos": (
                    r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE",
                ),
            },

            "powerpoint": {
                "apelidos": (
                    "powerpoint",
                    "power point",
                    "microsoft powerpoint",
                ),
                "caminhos": (
                    r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE",
                ),
            },

            "bloco de notas": {
                "apelidos": (
                    "bloco de notas",
                    "notepad",
                ),
                "caminhos": (
                    "notepad.exe",
                ),
            },

            "calculadora": {
                "apelidos": (
                    "calculadora",
                    "calc",
                ),
                "caminhos": (
                    "calc.exe",
                ),
            },
        }

    def abrir(self, programa: str) -> bool:
        """
        Abre um programa pelo nome principal ou por um apelido.
        """

        nome_principal = self.identificar(programa)

        if nome_principal is None:
            return False

        configuracao = self.programas[nome_principal]

        for caminho_original in configuracao["caminhos"]:
            caminho = os.path.expandvars(
                caminho_original
            )

            try:
                if self._eh_comando_windows(caminho):
                    subprocess.Popen(
                        [caminho],
                        shell=False
                    )

                    return True

                if Path(caminho).is_file():
                    os.startfile(caminho)

                    return True

            except Exception as erro:
                print(
                    f"Erro ao abrir '{nome_principal}' "
                    f"usando '{caminho}': {erro}"
                )

        return False

    def identificar(
        self,
        texto: str
    ) -> Optional[str]:
        """
        Identifica qual programa foi mencionado no texto.
        """

        texto = str(texto).lower().strip()

        if not texto:
            return None

        # Apelidos maiores são testados primeiro.
        candidatos = []

        for nome, configuracao in self.programas.items():
            for apelido in configuracao["apelidos"]:
                candidatos.append(
                    (apelido, nome)
                )

        candidatos.sort(
            key=lambda item: len(item[0]),
            reverse=True
        )

        for apelido, nome in candidatos:
            if apelido in texto:
                return nome

        return None

    def existe(self, programa: str) -> bool:
        return self.identificar(programa) is not None

    def listar(self) -> list[str]:
        return sorted(
            self.programas.keys()
        )

    @staticmethod
    def _eh_comando_windows(
        caminho: str
    ) -> bool:
        """
        Comandos como notepad.exe e calc.exe podem ser
        executados sem caminho absoluto.
        """

        return (
            "\\" not in caminho
            and "/" not in caminho
            and caminho.lower().endswith(".exe")
        )


programas = GerenciadorProgramas()