import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Ajustando ruído...")
    r.adjust_for_ambient_noise(source, duration=1)

    print("Fale algo...")
    audio = r.listen(source, timeout=5, phrase_time_limit=5)

print("⏳ Processando...")

try:
    texto = r.recognize_google(audio, language="pt-BR")
    print("Você disse:", texto)

except sr.UnknownValueError:
    print("Não entendi o áudio")

except sr.RequestError as e:
    print("Erro no serviço:", e)