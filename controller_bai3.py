import paho.mqtt.client as mqtt
import json
import threading

BROKER = "broker.emqx.io"
PORT = 1883

CMD_TOPIC = "iot/lab/light01/cmd"
STATUS_TOPIC = "iot/lab/light01/status"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

status_received = threading.Event()


def on_connect(client, userdata, flags, reason_code, properties):


    client.subscribe(STATUS_TOPIC)



def on_message(client, userdata, msg):
    payload = msg.payload.decode()

    try:
        data = json.loads(payload)

        print("Trang thai nhan duoc:")
        print(json.dumps(data, indent=2))

        # Bao cho vong while biet da nhan duoc trang thai
        status_received.set()

    except json.JSONDecodeError:
        print("Du lieu nhan duoc khong hop le.")


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

    # Xoa trang thai cu
    status_received.clear()

    client.publish(CMD_TOPIC, command)

    print(f"Da gui lenh {command} toi light01")

    # Cho den khi light01 gui status ve
    status_received.wait()


client.loop_stop()
client.disconnect()

print("Controller stopped.")