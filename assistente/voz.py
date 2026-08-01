import speech_recognition as sr
import pyttsx3


def criar_engine():
    engine = pyttsx3.init()
    engine.setProperty("rate", 180)
    return engine


def falar(texto: str) -> None:
    print("Jarvis:", texto)

    try:
        engine = criar_engine()
        engine.say(str(texto))
        engine.runAndWait()

    except Exception as erro:
        print(f"Erro na fala: {erro}")


def ouvir() -> str:
    reconhecedor = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎤 Ajustando microfone...")

            reconhecedor.adjust_for_ambient_noise(
                source,
                duration=1
            )

            reconhecedor.pause_threshold = 1.2
            reconhecedor.non_speaking_duration = 0.8

            print("🎤 Fale agora...")

            audio = reconhecedor.listen(
                source,
                timeout=10,
                phrase_time_limit=15
            )

        texto = reconhecedor.recognize_google(
            audio,
            language="pt-BR"
        )

        texto = texto.lower().strip()

        print("Você:", texto)

        return texto

    except sr.WaitTimeoutError:
        print("Nenhuma fala foi detectada.")
        return ""

    except sr.UnknownValueError:
        print("Não foi possível entender o áudio.")
        return ""

    except sr.RequestError as erro:
        print(f"Erro no serviço de reconhecimento: {erro}")
        return ""

    except OSError as erro:
        print(f"Erro ao acessar o microfone: {erro}")
        return ""

    except Exception as erro:
        print(f"Erro inesperado ao ouvir: {erro}")
        return ""