import webbrowser
from urllib.parse import quote_plus


def pesquisar(pergunta: str) -> str:
    pergunta = pergunta.strip()

    if not pergunta:
        return "Digite algo para eu pesquisar."

    termo = quote_plus(pergunta)
    url = f"https://www.google.com/search?q={termo}"

    webbrowser.open(url)

    return f"Pesquisando por '{pergunta}' no Google."