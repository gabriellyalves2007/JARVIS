import random
import subprocess
import webbrowser

from datetime import datetime

from assistente.ai import responder as responder_com_ia
from assistente.memoria import lembrar, obter

from ia.personalidade import personalidade
from servicos.internet import pesquisar_wiki


def abrir_google() -> str:
    webbrowser.open("https://google.com")

    resposta = personalidade.responder(
        "ABRIR_GOOGLE"
    )

    return resposta or "Abrindo o Google."


def abrir_youtube() -> str:
    webbrowser.open("https://youtube.com")

    resposta = personalidade.responder(
        "ABRIR_YOUTUBE"
    )

    return resposta or "Abrindo o YouTube."


def abrir_calculadora() -> str:
    try:
        subprocess.Popen(["calc.exe"])

        resposta = personalidade.responder(
            "ABRIR_CALCULADORA"
        )

        return resposta or "Abrindo a calculadora."

    except Exception as erro:
        print(
            "Erro ao abrir a calculadora: "
            f"{erro}"
        )

        resposta = personalidade.responder(
            "ERRO"
        )

        return resposta or (
            "Não consegui abrir a calculadora."
        )


def informar_horas() -> str:
    hora = datetime.now().strftime("%H:%M")

    respostas = (
        f"Agora são {hora}.",
        f"Neste momento são {hora}.",
        f"O relógio marca {hora}.",
        f"São exatamente {hora}.",
    )

    return random.choice(respostas)


def salvar_nome(comando: str) -> str:
    nome = str(comando)

    expressoes = (
        "meu nome é",
        "meu nome e",
        "eu me chamo",
        "pode me chamar de",
        "me chame de",
    )

    nome_minusculo = nome.lower()

    for expressao in expressoes:
        indice = nome_minusculo.find(expressao)

        if indice != -1:
            nome = nome[
                indice + len(expressao):
            ]

            break

    nome = nome.strip(" .,!?:;").title()

    if not nome:
        return "Não consegui identificar o seu nome."

    lembrar(
        "nome",
        nome
    )

    resposta = personalidade.responder(
        "SALVAR_NOME"
    )

    if not resposta:
        resposta = "Vou lembrar disso."

    return f"{resposta} Seu nome é {nome}."


def lembrar_nome() -> str:
    nome = obter("nome")

    if nome:
        respostas = (
            f"Seu nome é {nome}.",
            f"Você se chama {nome}.",
            f"Claro. Seu nome é {nome}.",
            f"Eu lembro. Você se chama {nome}.",
        )

        return random.choice(respostas)

    return "Ainda não sei o seu nome."


def limpar_pergunta(comando: str) -> str:
    """
    Remove expressões usadas para solicitar
    explicações ou pesquisas.
    """

    pergunta = str(comando).lower().strip()

    expressoes = (
        "quem é",
        "quem e",
        "quem foi",
        "o que é",
        "o que e",
        "o que são",
        "o que sao",
        "me explique",
        "explique",
        "fale sobre",
        "defina",
        "pesquise por",
        "pesquisar por",
        "pesquise",
        "pesquisar",
    )

    for expressao in expressoes:
        if pergunta.startswith(expressao):
            pergunta = pergunta[
                len(expressao):
            ].strip()

            break

    return pergunta.strip(
        " .,!?:;"
    )


def pesquisar(comando: str) -> str:
    """
    Procura uma resposta na Wikipédia.

    Caso a Wikipédia não encontre uma resposta,
    encaminha a pergunta para o módulo de IA.
    """

    pergunta = limpar_pergunta(
        comando
    )

    if not pergunta:
        return (
            "O que você gostaria que eu pesquisasse?"
        )

    print(
        f"🌐 Consultando Wikipédia: {pergunta}"
    )

    resposta_wikipedia = pesquisar_wiki(
        pergunta
    )

    if resposta_wikipedia:
        print(
            "✅ Resposta encontrada na Wikipédia."
        )

        return resposta_wikipedia

    print(
        "⚠️ Wikipédia não encontrou uma resposta."
    )

    print(
        "🧠 Encaminhando para o módulo de IA."
    )

    return responder_com_ia(
        pergunta
    )