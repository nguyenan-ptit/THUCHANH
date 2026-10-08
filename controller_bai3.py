import paho.mqtt.client as mqtt
import json

BROKER = "broker.emqx.io"
PORT = 1883

CMD_TOPIC = "iot/lab/light01/cmd"
STATUS_TOPIC = "iot/lab/light01/status"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, reason_code, properties):
    print("Controller connected to MQTT Broker")

    client.subscribe(STATUS_TOPIC)

    print(f"Subscribed to: {STATUS_TOPIC}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()

    data = json.loads(payload)

    print("Trang thai nhan duoc:")
    print(json.dumps(data, indent=2))

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

client.loop_start()

while True:
    command = input("Nhap lenh: ").strip().upper()

    if command == "EXIT":
        break

    if command not in ["ON", "OFF"]:
        print("Lenh khong hop le. Vui long nhap ON, OFF hoac EXIT.")
        continue

    client.publish(CMD_TOPIC, command)

    print(f"Da gui lenh {command} toi light01")


client.loop_stop()
client.disconnect()

print("Controller stopped.")
