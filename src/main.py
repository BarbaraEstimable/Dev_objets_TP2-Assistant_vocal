import subprocess
import speech_recognition as sr
from interpret_command import detecter_intention
from mqtt_assistant import publier_commande, lire_etat
from logger_mariadb import journaliser_commande

HOTWORD = "assistant"
MIC_INDEX = 1  # Yealink UH36


def speak(text, langue="fr", debit=150):
    lecture = subprocess.Popen(
        ["aplay"],
        stdin=subprocess.PIPE
    )

    audio = subprocess.run(
        ["espeak-ng", "-v", langue, "-s", str(debit), "--stdout", text],
        stdout=subprocess.PIPE,
        check=True
    )

    lecture.communicate(input=audio.stdout)


def ecouter_phrase(recognizer, micro, message_ecoute, timeout, phrase_time_limit):
    with sr.Microphone(device_index=micro) as source:
        print("Ne parle pas pendant 2 secondes...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print(message_ecoute)

        try:
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )
        except sr.WaitTimeoutError:
            print("Temps ecoule : aucune voix detectee")
            return None

    try:
        texte = recognizer.recognize_google(audio, language="fr-FR").lower()
        print("Texte capte :", texte)
        return texte
    except sr.UnknownValueError:
        print("Le systeme n'a pas compris")
        return None
    except sr.RequestError as e:
        print("Erreur du service STT :", e)
        return None


def main():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 1200
    r.pause_threshold = 0.8

    texte_hotword = ecouter_phrase(
        recognizer=r,
        micro=MIC_INDEX,
        message_ecoute="Dis le mot d'activation...",
        timeout=8,
        phrase_time_limit=3
    )

    if texte_hotword is None:
        return

    if HOTWORD not in texte_hotword:
        print("Hotword non detecte")
        return

    print("Hotword detecte")
    speak("Je vous ecoute")

    texte_commande = ecouter_phrase(
        recognizer=r,
        micro=MIC_INDEX,
        message_ecoute="Dis la commande...",
        timeout=8,
        phrase_time_limit=6
    )

    if texte_commande is None:
        speak("Je n ai pas compris la commande")
        return

    print("Commande finale :", texte_commande)
    intention = detecter_intention(texte_commande)
    print("Intention detectee :", intention)
    if intention == "allumer_lampe":
        publier_commande("on")
    elif intention == "eteindre_lampe":
        publier_commande("off")
    elif intention == "clignoter_lampe":
        publier_commande("blink")
    elif intention == "mode_nuit":
        publier_commande("night")
    if intention == "allumer_lampe":
        speak("Lampe allumee")
    elif intention == "eteindre_lampe":
        speak("Lampe eteinte")
    elif intention == "clignoter_lampe":
        speak("Clignotement active")
    elif intention == "etat_lampe":
        etat = lire_etat()

        if etat == "on":
            speak("La lampe est allumee")
        elif etat == "off":
            speak("La lampe est eteinte")
        elif etat == "blink":
            speak("La lampe est en clignotement")
        elif etat == "night":
            speak("La lampe est en mode nuit")
        else:
            speak("Je ne connais pas l etat actuel")

    resultat = "ok"

    if intention == "allumer_lampe":
        resultat = "on"
    elif intention == "eteindre_lampe":
        resultat = "off"
    elif intention == "clignoter_lampe":
        resultat = "blink"
    elif intention == "mode_nuit":
        resultat = "night"
    elif intention == "etat_lampe":
        resultat = "statut"
    else:
        resultat = "inconnue"

    journaliser_commande(texte_commande, intention, resultat)
    print("Commande journalisee en base")

if __name__ == "__main__":
    main()