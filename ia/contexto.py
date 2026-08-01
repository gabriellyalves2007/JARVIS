PALAVRAS_DE_CONTEXTO = {

    "ele",
    "ela",
    "isso",
    "aquilo",
    "aquele",
    "aquela",

    "primeiro",
    "segundo",
    "último",
    "ultimo",

    "novamente",
    "de novo",

    "também",
    "tambem",

    "outro",

    "esse",
    "essa",

    "anterior"
}


def usa_contexto(frase: str) -> bool:
    """
    Verifica se a frase provavelmente
    depende da conversa anterior.
    """

    frase = frase.lower()

    for palavra in PALAVRAS_DE_CONTEXTO:

        if palavra in frase:
            return True

    return False