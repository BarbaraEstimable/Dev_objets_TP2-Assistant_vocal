import json
import time
import paho.mqtt.client as mqtt
from gpiozero import LED

BROKER_HOST = "localhost"
BROKER_PORT = 1883
KEEPALIVE_S = 60

TEAM = "iot_supervise"
DEVICE = "pi_iot"

CLIENT_ID = "b3-lamp-pi_iot"

TOPIC_CMD = f"ahuntsic/aec-iot/b3/{TEAM}/{DEVICE}/actuators/lampe/cmd"
TOPIC_STATE = f"ahuntsic/aec-iot/b3/{TEAM}/{DEVICE}/actuators/lampe/state"

LED_PIN_BCM = 17
lampe = LED(LED_PIN_BCM)


def publier_etat(client, etat):
    client.publish(TOPIC_STATE, etat, qos=1, retain=True)
    print("Etat publie :", etat)


def executer_action(client, action):
    if action == "on":
        lampe.on()
        publier_etat(client, "on")

    elif action == "off":
        lampe.off()
        publier_etat(client, "off")

    elif action == "blink":
        for _ in range(6):
            lampe.on()
            time.sleep(0.3)
            lampe.off()
            time.sleep(0.3)
        publier_etat(client, "blink")

    elif action == "night":
        for _ in range(4):
            lampe.on()
            time.sleep(1.0)
            lampe.off()
            time.sleep(1.0)
        publier_etat(client, "night")

    else:
        print("Action inconnue :", action)


def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connecte au broker, code =", reason_code)
    if reason_code == 0:
        client.subscribe(TOPIC_CMD, qos=1)
        print("Abonne a :", TOPIC_CMD)


def on_message(client, userdata, msg):
    payload_text = msg.payload.decode("utf-8", errors="replace")
    print("Message recu :", payload_text)

    try:
        data = json.loads(payload_text)
    except json.JSONDecodeError:
        print("JSON invalide")
        return

    action = data.get("action")
    if not action:
        print("Aucune action recue")
        return

    executer_action(client, action)


def on_disconnect(client, userdata, reason_code, properties=None):
    print("Deconnecte du broker, code =", reason_code)


client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(BROKER_HOST, BROKER_PORT, keepalive=KEEPALIVE_S)
client.loop_forever()