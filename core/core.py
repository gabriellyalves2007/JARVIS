from core.pipeline import pipeline


def processar_entrada(texto: str) -> str:
    """
    Porta de entrada do JARVIS.

    Toda a inteligência passa
    pelo Pipeline.
    """

    return pipeline.executar(texto)