import paho.mqtt.client as mqtt
import json
import threading

BROKER = "broker.emqx.io"
PORT = 1883

CMD_TOPIC = "iot/lab/light01/cmd"
STATUS_TOPIC = "iot/lab/light01/status"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

status_received = threading.Event()
waiting_for_status = False
lock = threading.Lock()

def on_connect(client, userdata, flags, reason_code, properties):


    client.subscribe(STATUS_TOPIC)



def on_message(client, userdata, msg):
    global waiting_for_status

    try:
        data = json.loads(msg.payload.decode())

        if data.get("device_id") != "light01":
            return
        with lock:
            if not waiting_for_status:
                return
            waiting_for_status = False
            status_received.set()
        print("\nTrang thai nhan duoc:")
        print(json.dumps(data, indent=2))


    except json.JSONDecodeError:
        print("Du lieu nhan duoc khong hop le.")


client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)
client.loop_start()

try:
    while True:
        command = input("Nhap lenh: ").strip().upper()

        if command == "EXIT":
            break

        if command not in ["ON", "OFF"]:
            print("Lenh khong hop le. Vui long nhap ON, OFF hoac EXIT.")
            continue

        with lock:
            status_received.clear()
            waiting_for_status = True

        client.publish(CMD_TOPIC, command)

        print(f"Da gui lenh {command} toi light01")

        # Cho toi da 5 giay
        if not status_received.wait(timeout=5):
            with lock:
                waiting_for_status = False
            print("Khong nhan duoc trang thai tu light01.")

finally:
    client.loop_stop()
    client.disconnect()
    print("Controller stopped.")