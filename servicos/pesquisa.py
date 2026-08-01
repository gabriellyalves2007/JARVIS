import os
import webbrowser
from urllib.parse import quote_plus


def pesquisar(pergunta: str) -> str:
    """
    Abre uma pesquisa no Google usando o navegador padrão.
    """

    pergunta = str(pergunta).strip()

    if not pergunta:
        return "Digite algo para eu pesquisar."

    termo_codificado = quote_plus(pergunta)

    url = (
        "https://www.google.com/search"
        f"?q={termo_codificado}"
    )

    try:
        # Método mais confiável no Windows,
        # inclusive quando chamado por uma thread.
        os.startfile(url)

        return f"Pesquisando por '{pergunta}' no Google."

    except OSError as erro:
        print(f"Erro ao abrir pesquisa pelo Windows: {erro}")

        try:
            abriu = webbrowser.open(
                url,
                new=2,
                autoraise=True
            )

            if abriu:
                return f"Pesquisando por '{pergunta}' no Google."

        except Exception as erro_web:
            print(
                "Erro ao abrir pesquisa pelo navegador: "
                f"{erro_web}"
            )

    return "Não consegui abrir a pesquisa no navegador."