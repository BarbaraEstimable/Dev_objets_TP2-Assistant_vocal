# Dev_objets_TP2-Assistant_vocal

Projet 2 - Assistant vocal IoT sur Raspberry Pi

## Objectif

Ce projet realise un assistant vocal capable de :
- detecter un mot d activation
- ecouter une commande vocale
- interpreter l intention
- publier une commande MQTT
- controler une lampe / DEL
- publier le statut de la lampe
- journaliser les commandes dans MariaDB

## Modules

- `src/tts.py` : synthese vocale
- `src/stt.py` : reconnaissance vocale simple
- `src/hotword.py` : detection du mot d activation
- `src/interpret_command.py` : interpretation des commandes
- `src/mqtt_assistant.py` : publication MQTT
- `src/lamp_controller.py` : subscriber MQTT et controle de la DEL
- `src/logger_mariadb.py` : journalisation MariaDB
- `src/main.py` : orchestration generale

## Commandes vocales gerees

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

## Lancement

### 1. Lancer Mosquitto
```bash
sudo systemctl start mosquitto