from habilidades.base import Habilidade

from ia.acao_alvo import analisador

from servicos.janelas import janelas
from servicos.programas import programas


class HabilidadePrograma(Habilidade):
    """
    Controla programas e janelas do Windows.

    Ações disponíveis:
    - abrir;
    - fechar;
    - reiniciar;
    - minimizar;
    - maximizar;
    - restaurar;
    - focar.
    """

    ACOES_JANELA = {
        "minimizar",
        "maximizar",
        "restaurar",
        "focar",
    }

    def executar(
        self,
        comando: str = ""
    ) -> str:
        acao_alvo = analisador.analisar(
            comando
        )

        if acao_alvo is None:
            # Compatibilidade com o comportamento
            # antigo, que abria o programa mencionado.
            return self._abrir_comando_antigo(
                comando
            )

        acao = acao_alvo.acao
        alvo_original = acao_alvo.alvo

        nome_programa = programas.identificar(
            alvo_original
        )

        if acao in {
            "abrir",
            "fechar",
            "reiniciar",
        }:
            if nome_programa is None:
                return (
                    "Não consegui identificar "
                    f"o programa '{alvo_original}'."
                )

            sucesso = self._executar_programa(
                acao=acao,
                programa=nome_programa
            )

            nome_exibicao = self._formatar_nome(
                nome_programa
            )

        elif acao in self.ACOES_JANELA:
            termo_janela = self._obter_termo_janela(
                nome_programa,
                alvo_original
            )

            sucesso = self._executar_janela(
                acao=acao,
                termo=termo_janela
            )

            nome_exibicao = (
                self._formatar_nome(nome_programa)
                if nome_programa
                else alvo_original.title()
            )

        else:
            return (
                f"A ação '{acao}' ainda "
                "não é suportada."
            )

        if sucesso:
            return self._mensagem_sucesso(
                acao=acao,
                nome=nome_exibicao
            )

        return self._mensagem_falha(
            acao=acao,
            nome=nome_exibicao
        )

    def _abrir_comando_antigo(
        self,
        comando: str
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

        nome_exibicao = self._formatar_nome(
            nome_programa
        )

        if abriu:
            return f"Abrindo {nome_exibicao}."

        return (
            f"Encontrei o programa "
            f"'{nome_exibicao}', "
            "mas não consegui abri-lo."
        )

    @staticmethod
    def _executar_programa(
        acao: str,
        programa: str
    ) -> bool:
        if acao == "abrir":
            return programas.abrir(
                programa
            )

        if acao == "fechar":
            return programas.fechar(
                programa
            )

        if acao == "reiniciar":
            return programas.reiniciar(
                programa
            )

        return False

    @staticmethod
    def _executar_janela(
        acao: str,
        termo: str
    ) -> bool:
        if acao == "minimizar":
            return janelas.minimizar(
                termo
            )

        if acao == "maximizar":
            return janelas.maximizar(
                termo
            )

        if acao == "restaurar":
            return janelas.restaurar(
                termo
            )

        if acao == "focar":
            return janelas.focar(
                termo
            )

        return False

    @staticmethod
    def _obter_termo_janela(
        nome_programa,
        alvo_original: str
    ) -> str:
        """
        Converte o nome interno do programa
        em um termo provável do título da janela.
        """

        termos = {
            "chrome": "Chrome",
            "edge": "Edge",
            "firefox": "Firefox",
            "vscode": "Visual Studio Code",
            "spotify": "Spotify",
            "word": "Word",
            "excel": "Excel",
            "powerpoint": "PowerPoint",
            "bloco de notas": "Bloco de Notas",
            "calculadora": "Calculadora",
            "whatsapp": "WhatsApp",
        }

        if nome_programa:
            return termos.get(
                nome_programa,
                nome_programa
            )

        return alvo_original

    @staticmethod
    def _mensagem_sucesso(
        acao: str,
        nome: str
    ) -> str:
        mensagens = {
            "abrir": f"Abrindo {nome}.",
            "fechar": f"{nome} foi fechado.",
            "reiniciar": f"{nome} foi reiniciado.",
            "minimizar": f"{nome} foi minimizado.",
            "maximizar": f"{nome} foi maximizado.",
            "restaurar": f"{nome} foi restaurado.",
            "focar": (
                f"{nome} foi trazido "
                "para primeiro plano."
            ),
        }

        return mensagens.get(
            acao,
            f"Ação concluída em {nome}."
        )

    @staticmethod
    def _mensagem_falha(
        acao: str,
        nome: str
    ) -> str:
        return (
            f"Não consegui {acao} {nome}. "
            "Verifique se o programa ou "
            "a janela está disponível."
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
            "whatsapp": "WhatsApp",
        }

        return nomes_especiais.get(
            nome,
            nome.title()
        )


programa = HabilidadePrograma()