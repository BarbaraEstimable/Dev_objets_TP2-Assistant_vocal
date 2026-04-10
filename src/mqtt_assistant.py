import json
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
KEEPALIVE_S = 60

TEAM = "iot_supervise"
DEVICE = "pi_iot"

CLIENT_ID = "b3-assistant-pi_iot"

TOPIC_CMD = f"ahuntsic/aec-iot/b3/{TEAM}/{DEVICE}/actuators/lampe/cmd"


def publier_commande(action):
    client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=KEEPALIVE_S)

    payload = {
        "action": action
    }

    message = json.dumps(payload)
    client.publish(TOPIC_CMD, message, qos=1)
    client.disconnect()

    print("Topic publie :", TOPIC_CMD)
    print("Message publie :", message)

def lire_etat():
    etat_recu = {"valeur": None}

    topic_state = f"ahuntsic/aec-iot/b3/{TEAM}/{DEVICE}/actuators/lampe/state"

    def on_message(client, userdata, msg):
        etat_recu["valeur"] = msg.payload.decode("utf-8", errors="replace")
        client.disconnect()

    client = mqtt.Client(client_id="b3-etat-pi_iot", protocol=mqtt.MQTTv311)
    client.on_message = on_message
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=KEEPALIVE_S)
    client.subscribe(topic_state, qos=1)
    client.loop_forever()

    return etat_recu["valeur"]

if __name__ == "__main__":
    publier_commande("on")