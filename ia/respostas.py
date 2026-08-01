from datetime import datetime

from ia.personalidade import resposta


def responder_horas():

    hora = datetime.now().strftime("%H:%M")

    frases = (

        f"Agora são {hora}.",

        f"Neste momento são {hora}.",

        f"O relógio marca {hora}.",

        f"São exatamente {hora}."
    )

    import random

    return random.choice(frases)