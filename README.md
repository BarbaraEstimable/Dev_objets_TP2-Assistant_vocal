# Dev_objets_TP2-Assistant_vocal

Projet 2 - Assistant vocal IoT sur Raspberry Pi

## Objectif

Ce projet realise un assistant vocal capable de :
- detecter un mot d activation
- ecouter une commande vocale
- interpreter l'intention
- publier une commande MQTT
- controler une lampe / DEL
- publier le statut de la lampe
- convertir l'audio et le texte
- fournir un retour vocal
- journaliser les commandes dans MariaDB

## Le fonctionnement attendu
- l’utilisateur prononce le mot d’activation
- le système confirme qu’il est en écoute
- l’utilisateur prononce une commande
- la commande est transcrite en texte
- l’intention est déterminée
- l’action est publiée sur MQTT
- un composant ou subscriber exécute l’action sur la lampe
- le système retourne un message vocal ou texte de confirmation
- une trace minimale de la commande est conservée

## Modules

- `src/tts.py` : synthese vocale
- `src/stt.py` : reconnaissance vocale simple
- `src/hotword.py` : detection du mot d activation
- `src/interpret_command.py` : interpretation des commandes
- `src/mqtt_assistant.py` : publication MQTT
- `src/lamp_controller.py` : subscriber MQTT et controle de la DEL(GPIO)
- `src/logger_mariadb.py` : journalisation MariaDB
- `src/main.py` : orchestration generale

## Commandes vocales gerees et obligatoires
- allume la lampe
- eteins la lampe
- fais clignoter la lampe
- donne moi le statut
- active le mode nuit

## Technologies utilisees

- Python
- SpeechRecognition
- espeak-ng
- paho-mqtt
- Mosquitto
- gpiozero
- MariaDB
- NLTK

## Topics MQTT

- commande :
  `ahuntsic/aec-iot/b3/iot_supervise/pi_iot/actuators/lampe/cmd`
- statut :
  `ahuntsic/aec-iot/b3/iot_supervise/pi_iot/actuators/lampe/state`

## Base de donnees

Base :
- `iot_supervise`

Table :
- `commandes_vocales`

Champs journalises :
- date et heure
- texte_commande
- intention
- resultat

## Branchement DEL

- GPIO BCM 17
- resistance 220 ohms ou 330 ohms
- patte longue DEL -> GPIO 17 via resistance
- patte courte DEL -> GND

## Matériel requis
- Un Raspberry Pi (de préférence 4 et plus)
- Pour entendre la voix, il faut:
    - soit  un écran HDMI avec haut-parleurs ;
    - soit un haut-parleur USB ;
    - soit un casque USB. 

## Lancement

### 1. Brancher votre matériel
À votre Raspberry Pi, vous devez brancher un écran HDMI avec haut-parleurs ou un haut-parleur USB ou  un casque USB.

### 2. Importer les bibliothèques nécessaires et crée un environnement virtuelle
- Installer Mosquitto et l'importer
- Vérifier le MQTT
- Créer un environnement virtuel(venv)

### 3. Ouvrir 4 terminaux du Raspberry Pi
- un pour mqtt_assistant.py
- un pour lamp_controller.py
- un autre pour logger_mariadb.py
- et pour finir un pour main.py (ce qui va déclencher l'assistant vocal).
