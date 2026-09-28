import paho.mqtt.client as mqtt
from datetime import datetime

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "iot/lab/message"


def on_connect(client, userdata, flags, reson_code, properties):
    if reson_code == 0:
        print("Ket noi MQTT broker thanh cong")
        client.subscribe(TOPIC)
        print("Dang lang nghe topic:", TOPIC)
    else:
        print("Ket noi that bai, ma loi:", reson_code)


def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    current_time = datetime.now().strftime("%H:%M:%S")

    print("\nNhan duoc message")
    print("Topic:", msg.topic)
    print("Payload:", payload)
    print("Time:", current_time)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

print("Subscriber dang chay....")
print("Nhan Ctrl+C de dung chuong trinh.")

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nDa dung Subscriber.")
    client.disconnect()
