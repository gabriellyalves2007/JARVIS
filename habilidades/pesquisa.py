from habilidades.base import Habilidade

from assistente.comandos import pesquisar as pesquisar_wikipedia
from servicos.pesquisa import pesquisar as pesquisar_google

from ia.interpretador import interpretador


class Pesquisa(Habilidade):
    """
    Decide entre:

    - abrir uma pesquisa no Google;
    - consultar informações na Wikipédia.
    """

    def executar(
        self,
        comando: str = ""
    ) -> str:

        texto = interpretador.interpretar(comando)

        comandos_google = (
            "pesquise",
            "pesquisar",
            "procure",
            "buscar",
            "busque",
            "pesquisa por",
        )

        if any(
            expressao in texto
            for expressao in comandos_google
        ):
            termo = self.extrair_termo(comando)

            if not termo:
                return "O que você gostaria que eu pesquisasse?"

            return pesquisar_google(termo)

        return pesquisar_wikipedia(comando)

    @staticmethod
    def extrair_termo(comando: str) -> str:
        termo = comando.strip()

        expressoes = (
            "pesquise por",
            "pesquisar por",
            "pesquisa por",
            "procure por",
            "buscar por",
            "busque por",
            "pesquise",
            "pesquisar",
            "procure",
            "buscar",
            "busque",
        )

        termo_minusculo = termo.lower()

        for expressao in expressoes:
            if termo_minusculo.startswith(expressao):
                termo = termo[
                    len(expressao):
                ].strip()

                break

        return termo


pesquisa = Pesquisa()