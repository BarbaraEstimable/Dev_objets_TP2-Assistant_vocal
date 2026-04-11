import speech_recognition as sr

HOTWORD = "assistant"

r = sr.Recognizer()
r.dynamic_energy_threshold = False
r.energy_threshold = 1200
r.pause_threshold = 0.8

MIC_INDEX = 1  # Yealink UH36

with sr.Microphone(device_index=MIC_INDEX) as source:
    print("Ne parle pas pendant 2 secondes...")
    r.adjust_for_ambient_noise(source, duration=2)
    print("Dis le mot d activation...")

    try:
        audio = r.listen(source, timeout=8, phrase_time_limit=3)
    except sr.WaitTimeoutError:
        print("Temps ecoule : aucune voix detectee")
        raise SystemExit

try:
    texte = r.recognize_google(audio, language="fr-FR").lower()
    print("Texte capte :", texte)

    if HOTWORD in texte:
        print("Hotword detecte")
    else:
        print("Hotword non detecte")

except sr.UnknownValueError:
    print("Le systeme n a pas compris")
except sr.RequestError as e:
    print("Erreur du service STT :", e)