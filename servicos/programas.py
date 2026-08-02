import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional


class GerenciadorProgramas:
    """
    Localiza, abre, fecha e reinicia
    programas cadastrados no Windows.
    """

    def __init__(self):
        self.programas = {
            "chrome": {
                "processo": "chrome.exe",
                "apelidos": (
                    "chrome",
                    "google chrome",
                ),
                "comandos": (
                    "chrome.exe",
                ),
                "caminhos": (
                    r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe",
                    r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe",
                    r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe",
                ),
                "uris": (),
            },

            "edge": {
                "processo": "msedge.exe",
                "apelidos": (
                    "edge",
                    "microsoft edge",
                ),
                "comandos": (
                    "msedge.exe",
                ),
                "caminhos": (
                    r"%PROGRAMFILES%\Microsoft\Edge\Application\msedge.exe",
                    r"%PROGRAMFILES(X86)%\Microsoft\Edge\Application\msedge.exe",
                ),
                "uris": (
                    "microsoft-edge:",
                ),
            },

            "firefox": {
                "processo": "firefox.exe",
                "apelidos": (
                    "firefox",
                    "mozilla",
                    "mozilla firefox",
                ),
                "comandos": (
                    "firefox.exe",
                ),
                "caminhos": (
                    r"%PROGRAMFILES%\Mozilla Firefox\firefox.exe",
                    r"%PROGRAMFILES(X86)%\Mozilla Firefox\firefox.exe",
                ),
                "uris": (),
            },

            "vscode": {
                "processo": "Code.exe",
                "apelidos": (
                    "vscode",
                    "vs code",
                    "visual studio code",
                    "code",
                ),
                "comandos": (
                    "code.exe",
                    "code",
                ),
                "caminhos": (
                    r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe",
                    r"%PROGRAMFILES%\Microsoft VS Code\Code.exe",
                    r"%PROGRAMFILES(X86)%\Microsoft VS Code\Code.exe",
                ),
                "uris": (),
            },

            "spotify": {
                "processo": "Spotify.exe",
                "apelidos": (
                    "spotify",
                ),
                "comandos": (
                    "Spotify.exe",
                    "spotify.exe",
                ),
                "caminhos": (
                    r"%LOCALAPPDATA%\Microsoft\WindowsApps\Spotify.exe",
                    r"%APPDATA%\Spotify\Spotify.exe",
                ),
                "uris": (
                    "spotify:",
                ),
            },

            "word": {
                "processo": "WINWORD.EXE",
                "apelidos": (
                    "word",
                    "microsoft word",
                ),
                "comandos": (
                    "winword.exe",
                ),
                "caminhos": (
                    r"%PROGRAMFILES%\Microsoft Office\root\Office16\WINWORD.EXE",
                    r"%PROGRAMFILES(X86)%\Microsoft Office\root\Office16\WINWORD.EXE",
                ),
                "uris": (),
            },

            "excel": {
                "processo": "EXCEL.EXE",
                "apelidos": (
                    "excel",
                    "microsoft excel",
                ),
                "comandos": (
                    "excel.exe",
                ),
                "caminhos": (
                    r"%PROGRAMFILES%\Microsoft Office\root\Office16\EXCEL.EXE",
                    r"%PROGRAMFILES(X86)%\Microsoft Office\root\Office16\EXCEL.EXE",
                ),
                "uris": (),
            },

            "powerpoint": {
                "processo": "POWERPNT.EXE",
                "apelidos": (
                    "powerpoint",
                    "power point",
                    "microsoft powerpoint",
                ),
                "comandos": (
                    "powerpnt.exe",
                ),
                "caminhos": (
                    r"%PROGRAMFILES%\Microsoft Office\root\Office16\POWERPNT.EXE",
                    r"%PROGRAMFILES(X86)%\Microsoft Office\root\Office16\POWERPNT.EXE",
                ),
                "uris": (),
            },

            "bloco de notas": {
                "processo": "notepad.exe",
                "apelidos": (
                    "bloco de notas",
                    "notepad",
                ),
                "comandos": (
                    "notepad.exe",
                ),
                "caminhos": (),
                "uris": (),
            },

            "calculadora": {
                "processo": "CalculatorApp.exe",
                "apelidos": (
                    "calculadora",
                    "calc",
                ),
                "comandos": (
                    "calc.exe",
                ),
                "caminhos": (),
                "uris": (
                    "calculator:",
                ),
            },

            "whatsapp": {
                "processo": "WhatsApp.exe",
                "apelidos": (
                    "whatsapp",
                    "whats app",
                ),
                "comandos": (
                    "WhatsApp.exe",
                ),
                "caminhos": (
                    r"%LOCALAPPDATA%\WhatsApp\WhatsApp.exe",
                    r"%LOCALAPPDATA%\Microsoft\WindowsApps\WhatsApp.exe",
                ),
                "uris": (
                    "whatsapp:",
                ),
            },
        }

    def identificar(
        self,
        texto: str
    ) -> Optional[str]:
        texto = str(texto).lower().strip()

        if not texto:
            return None

        candidatos = []

        for nome, dados in self.programas.items():
            for apelido in dados["apelidos"]:
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

    def existe(
        self,
        programa: str
    ) -> bool:
        """
        Verifica se o texto menciona
        um programa conhecido.
        """

        return self.identificar(programa) is not None

    def abrir(
        self,
        programa: str
    ) -> bool:
        nome = (
            self.identificar(programa)
            or str(programa).lower().strip()
        )

        if nome not in self.programas:
            return False

        dados = self.programas[nome]

        # Primeiro procura o comando no PATH.
        for comando in dados.get("comandos", ()):
            executavel = shutil.which(comando)

            if executavel is None:
                continue

            try:
                subprocess.Popen(
                    [executavel],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

                return True

            except OSError as erro:
                print(
                    f"Erro ao executar "
                    f"'{executavel}': {erro}"
                )

        # Depois tenta caminhos conhecidos.
        for caminho_original in dados.get(
            "caminhos",
            ()
        ):
            caminho = os.path.expandvars(
                caminho_original
            )

            if not Path(caminho).is_file():
                continue

            try:
                os.startfile(caminho)

                return True

            except OSError as erro:
                print(
                    f"Erro ao abrir "
                    f"'{caminho}': {erro}"
                )

        # Por último tenta protocolos do Windows.
        for uri in dados.get("uris", ()):
            try:
                os.startfile(uri)

                return True

            except OSError as erro:
                print(
                    f"Erro ao abrir "
                    f"o protocolo '{uri}': {erro}"
                )

        return False

    def fechar(
        self,
        programa: str
    ) -> bool:
        nome = (
            self.identificar(programa)
            or str(programa).lower().strip()
        )

        if nome not in self.programas:
            return False

        processo = self.programas[
            nome
        ]["processo"]

        try:
            resultado = subprocess.run(
                [
                    "taskkill",
                    "/F",
                    "/IM",
                    processo,
                ],
                capture_output=True,
                text=True,
                check=False
            )

            return resultado.returncode == 0

        except OSError as erro:
            print(
                f"Erro ao fechar "
                f"'{nome}': {erro}"
            )

            return False

    def reiniciar(
        self,
        programa: str
    ) -> bool:
        nome = (
            self.identificar(programa)
            or str(programa).lower().strip()
        )

        if nome not in self.programas:
            return False

        self.fechar(nome)

        return self.abrir(nome)

    def listar(self) -> list[str]:
        return sorted(
            self.programas.keys()
        )


programas = GerenciadorProgramas()