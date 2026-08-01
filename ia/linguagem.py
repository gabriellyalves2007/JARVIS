import re
import unicodedata


def normalizar(texto: str) -> str:
    """
    Normaliza qualquer frase recebida pelo Jarvis.
    """

    texto = texto.lower().strip()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        c
        for c in texto
        if unicodedata.category(c) != "Mn"
    )

    texto = re.sub(
        r"[^\w\s]",
        "",
        texto
    )

    texto = " ".join(texto.split())

    return texto


def contem(texto: str, palavras) -> bool:
    return any(
        palavra in texto
        for palavra in palavras
    )