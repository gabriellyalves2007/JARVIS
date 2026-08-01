from core.intencoes import Intencao
from habilidades.base import Habilidade
from servicos.programas import programas


class HabilidadePrograma(Habilidade):
    """
    Habilidade responsável por abrir qualquer
    programa cadastrado no serviço do Windows.
    """

    def executar(
        self,
        comando: str = ""
    ) -> str:
        nome_programa = programas.identificar(
            comando
        )

        if nome_programa is None:
            disponiveis = ", ".join(
                programas.listar()
            )

            return (
                "Não consegui identificar o programa. "
                f"Atualmente conheço: {disponiveis}."
            )

        abriu = programas.abrir(
            nome_programa
        )

        if abriu:
            nome_exibicao = self._formatar_nome(
                nome_programa
            )

            return (
                f"Abrindo {nome_exibicao}."
            )

        return (
            f"Encontrei o programa '{nome_programa}', "
            "mas não consegui abri-lo. "
            "Talvez o caminho precise ser configurado."
        )

    @staticmethod
    def _formatar_nome(
        nome: str
    ) -> str:
        nomes_especiais = {
            "vscode": "VS Code",
            "chrome": "Google Chrome",
            "edge": "Microsoft Edge",
            "firefox": "Firefox",
            "spotify": "Spotify",
            "word": "Microsoft Word",
            "excel": "Microsoft Excel",
            "powerpoint": "PowerPoint",
            "bloco de notas": "Bloco de Notas",
            "calculadora": "Calculadora",
        }

        return nomes_especiais.get(
            nome,
            nome.title()
        )


programa = HabilidadePrograma()