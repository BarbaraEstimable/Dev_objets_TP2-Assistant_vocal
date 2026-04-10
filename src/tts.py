import subprocess

def speak(text, langue="fr", debit=150):
    """
    Fait parler le Raspberry Pi avec espeak-ng.
    text   : texte � prononcer
    langue : voix/langue (ex. fr)
    debit  : vitesse de parole
    """
    subprocess.run(
        ["espeak-ng", "-v", langue, "-s", str(debit), "--stdout", text],
        stdout=subprocess.PIPE,
        check=True
    )

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


if __name__ == "__main__":
    speak("Bonjour")
    speak("Le Raspberry Pi parle")
    speak("Test de la voix")