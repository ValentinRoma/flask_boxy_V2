import os
import time 
from app import create_app, db
import paho.mqtt.client as mqtt
import json
from app import states
import threading 


MQTT_broker = "bb19c2482bdd418ca43217f30c6ea2f9.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "IgnacioValentin"
MQTT_PASS = "12345678vR"
MQTT_TOPIC_DATAS = f'{states.clave_boxy}/datas'

current_topic = None
# Definiendo un callback:

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT ✅")
        # Nos suscribimos a un topic inicial (si está definido)
        global current_topic
        if states.clave_boxy:
            current_topic = f"{states.clave_boxy}/datas"
            client.subscribe(current_topic)
            print(f"Suscrito a {current_topic}")
    else:
        print(f"Error de conexión al broker, código {rc}")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        states.temperatura = data["temperatura"]
        states.humedad = data["humedad"]
        print(f"Temperatura: {states.temperatura}°C, Humedad: {states.humedad}%")
    except Exception as e:
        print("Error procesando mensaje:", e)
        
        
# Crear un client MQTT:
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.tls_set()

# Asignamos el callback:

client.on_connect = on_connect
client.on_message = on_message

# Conectando al broker:
client.connect(MQTT_broker, MQTT_PORT, 60)

#Dejar la conexión en loop:
client.loop_start()

act = 'ON_ENGINE'



# Publicador:
def publish_funct():
    try:
        while True:
            if states.clave_boxy:
                topic_act = f"{states.clave_boxy}/actuando"
                client.publish(topic_act, states.actuator)
                print(f"[PUB] {states.actuator} → {topic_act}")
            time.sleep(.01)
    except KeyboardInterrupt:
        print("Desconectado del broker")
        client.loop_stop()
        client.disconnect()
        

        
# Actualizando Suscripción:
def update_subscription():
    global current_topic
    while True:
        if states.clave_boxy:
            new_topic = f"{states.clave_boxy}/datas"
            if new_topic != current_topic:
                # Cambió el topic → desuscribirse y suscribirse
                if current_topic:
                    client.unsubscribe(current_topic)
                    print(f"Desuscrito de {current_topic}")
                client.subscribe(new_topic)
                print(f"Suscrito a {new_topic}")
                current_topic = new_topic
        time.sleep(5)  # chequeo cada 5 segundos


threading.Thread(target=publish_funct, daemon=True).start()
threading.Thread(target=update_subscription, daemon=True).start()

 
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()