import paho.mqtt.client as mqtt
import json 

BROKER = "localhost"
PORT = 1883

CMD_TOPIC = "iot/lab/light01/cmd"
STATUS_TOPIC = "iot/lab/light01/status"

DEVICE_ID = "light01"

light_status = "OFF"
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected with result code " + str(reason_code))

    client.subscribe(CMD_TOPIC)

    print(f"Subscribed to topic: {CMD_TOPIC}")

def on_message(client, userdata, msg):
    global light_status

    command = msg.payload.decode().strip()

    print(f"Received command: {command}")

    if command == "ON":
        light_status = "ON"

    elif command == "OFF":
        light_status = "OFF"

    else:
        print("Invalid command")
        return

    status_data = {
        "device_id": DEVICE_ID,
        "status": light_status
    }

    payload = json.dumps(status_data)

    client.publish(STATUS_TOPIC, payload)

    print(f"Published status: {payload}")

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

print("Smart Light Device is running...")

client.loop_forever()