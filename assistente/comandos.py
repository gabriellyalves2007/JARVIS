import subprocess
import webbrowser

from datetime import datetime

from assistente.memoria import lembrar, obter
from servicos.internet import pesquisar_wiki

from ia.personalidade import personalidade


def abrir_google() -> str:
    webbrowser.open("https://google.com")

    return personalidade.responder(
        "ABRIR_GOOGLE"
    )


def abrir_youtube() -> str:
    webbrowser.open("https://youtube.com")

    return personalidade.responder(
        "ABRIR_YOUTUBE"
    )


def abrir_calculadora() -> str:

    try:
        subprocess.Popen(["calc.exe"])

        return personalidade.responder(
            "ABRIR_CALCULADORA"
        )

    except Exception:

        return personalidade.responder(
            "ERRO"
        )


def informar_horas() -> str:

    hora = datetime.now().strftime("%H:%M")

    respostas = (

        f"Agora são {hora}.",

        f"Neste momento são {hora}.",

        f"O relógio marca {hora}.",

        f"São exatamente {hora}."
    )

    import random

    return random.choice(respostas)


def salvar_nome(comando: str) -> str:

    nome = comando.lower()

    for texto in (
        "meu nome é",
        "meu nome e",
        "eu me chamo",
    ):
        nome = nome.replace(
            texto,
            ""
        )

    nome = nome.strip().title()

    if not nome:
        return "Não consegui identificar o seu nome."

    lembrar(
        "nome",
        nome
    )

    resposta = personalidade.responder(
        "SALVAR_NOME"
    )

    return f"{resposta} Seu nome é {nome}."


def lembrar_nome() -> str:

    nome = obter("nome")

    if nome:

        respostas = (

            f"Seu nome é {nome}.",

            f"Você se chama {nome}.",

            f"Claro. Seu nome é {nome}.",

            f"Eu lembro. Você se chama {nome}."
        )

        import random

        return random.choice(
            respostas
        )

    return (
        "Ainda não sei o seu nome."
    )


def pesquisar(comando: str) -> str:

    pergunta = comando.lower()

    for palavra in (

        "quem é",

        "quem foi",

        "o que é",

        "o que sao",

        "explique",

        "pesquise",

        "pesquisar",

    ):

        pergunta = pergunta.replace(
            palavra,
            ""
        )

    pergunta = pergunta.replace(
        "?",
        ""
    ).strip()

    if not pergunta:

        return (
            "O que você gostaria que eu pesquisasse?"
        )

    resposta = pesquisar_wiki(
        pergunta
    )

    if resposta:
        return resposta

    return (
        "Não encontrei informações sobre isso."
    )