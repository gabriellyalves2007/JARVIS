import speech_recognition as sr

from voz import falar
from core import processar_entrada


WAKE_WORDS = (
    "jarvis",
    "hey jarvis",
    "ei jarvis"
)

COMANDOS_DESLIGAR = (
    "desligar jarvis",
    "parar jarvis"
)


def ouvir_continuo():
    """Mantém o Jarvis ouvindo continuamente."""

    reconhecedor = sr.Recognizer()

    with sr.Microphone() as microfone:

        reconhecedor.adjust_for_ambient_noise(microfone)

        print("🎧 Jarvis está ouvindo...")

        while True:

            try:

                audio = reconhecedor.listen(
                    microfone,
                    phrase_time_limit=6
                )

                texto = reconhecedor.recognize_google(
                    audio,
                    language="pt-BR"
                ).lower()

                print(f"👤 Você: {texto}")

                if any(comando in texto for comando in COMANDOS_DESLIGAR):
                    falar("Desligando.")
                    break

                if any(wake in texto for wake in WAKE_WORDS):

                    comando = texto

                    for wake in WAKE_WORDS:
                        comando = comando.replace(wake, "")

                    comando = comando.strip()

                    if not comando:
                        falar("Sim?")
                        continue

                    resposta = processar_entrada(comando)

                    if resposta:
                        falar(str(resposta)[:300])

            except sr.UnknownValueError:
                continue

            except Exception as erro:
                print(f"Erro: {erro}")