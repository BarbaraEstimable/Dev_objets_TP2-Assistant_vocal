import re
from nltk.tokenize import word_tokenize


def normaliser_texte(texte):
    """
    Met le texte en minuscules et enleve les espaces inutiles.
    """
    return texte.lower().strip()


def est_commande_allumer(texte):
    """
    Detecte une commande pour allumer la lampe.
    """
    motif = r"(allume|active|mets)\s+(la\s+)?lampe"
    return re.search(motif, texte) is not None


def est_commande_eteindre(texte):
    """
    Detecte une commande pour eteindre la lampe.
    """
    motif = r"(eteins|arrete|coupe)\s+(la\s+)?lampe"
    return re.search(motif, texte) is not None


def est_commande_clignoter(texte):
    """
    Detecte une commande pour faire clignoter la lampe.
    """
    motif = r"(clignote|clignoter|fais\s+clignoter)\s+(la\s+)?lampe"
    return re.search(motif, texte) is not None


def est_commande_etat(texte):
    """
    Detecte une commande pour demander le statut de la lampe.
    """
    texte = texte.lower().strip()

    if "donne moi le statut" in texte:
        return True
    if "donne-moi le statut" in texte:
        return True
    if "quel est le statut" in texte:
        return True
    if "statut de la lampe" in texte:
        return True
    if texte == "statut":
        return True

    return False


def est_commande_mode_nuit(texte):
    """
    Detecte une commande pour activer le mode nuit.
    """
    motif = r"((active|mets)\s+(le\s+)?mode\s+nuit|mode\s+nuit)"
    return re.search(motif, texte) is not None


def detecter_intention(texte):
    """
    Retourne l intention principale a partir du texte.
    """
    texte = normaliser_texte(texte)
    tokens = word_tokenize(texte, language="french")
    tokens = [mot.lower() for mot in tokens]

    if est_commande_mode_nuit(texte):
        return "mode_nuit"

    if est_commande_clignoter(texte):
        return "clignoter_lampe"

    if est_commande_etat(texte):
        return "etat_lampe"

    if est_commande_eteindre(texte):
        return "eteindre_lampe"

    if est_commande_allumer(texte):
        return "allumer_lampe"

    return "inconnue"


if __name__ == "__main__":
    commandes = [
        "allume la lampe",
        "eteins la lampe",
        "fais clignoter la lampe",
        "donne moi le statut",
        "statut",
        "active le mode nuit",
        "bonjour",
    ]

    for commande in commandes:
        intention = detecter_intention(commande)
        print(f"Commande : {commande}")
        print(f"Intention : {intention}")
        print("-" * 40)