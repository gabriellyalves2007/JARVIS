import speech_recognition as sr
from core import processar_entrada
from voz import falar


def ouvir_wake():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        r.adjust_for_ambient_noise(source)
        print("🎧 Aguardando 'Hey Jarvis'...")

        while True:
            try:
                audio = r.listen(source)
                texto = r.recognize_google(audio, language="pt-BR").lower()

                print("Você:", texto)

                if "hey jarvis" in texto or "ei jarvis" in texto:

                    comando = texto.replace("hey jarvis", "").replace("ei jarvis", "").strip()

                    if not comando:
                        falar("Sim?")
                        continue

                    resposta = processar_entrada(comando)

                    falar(resposta)

            except:
                continue