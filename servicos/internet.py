import wikipedia

wikipedia.set_lang("pt")


def pesquisar_wiki(pergunta: str):
    try:
        return wikipedia.summary(
            pergunta,
            sentences=3
        )

    except wikipedia.exceptions.DisambiguationError:
        return "Encontrei vários resultados. Seja mais específico."

    except wikipedia.exceptions.PageError:
        return None

    except Exception as erro:
        print(f"Erro ao pesquisar na Wikipédia: {erro}")
        return None