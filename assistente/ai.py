def responder(pergunta: str) -> str:
    """
    Resposta alternativa quando os serviços locais
    não conseguem encontrar uma informação.

    Futuramente, este método poderá ser conectado
    ao OpenAI, Gemini, Ollama ou outro modelo.
    """

    pergunta = str(pergunta).strip()

    if not pergunta:
        return "Não recebi uma pergunta para responder."

    return (
        "Ainda não encontrei uma resposta confiável para "
        f"'{pergunta}'. Minha inteligência artificial ainda "
        "não foi integrada."
    )