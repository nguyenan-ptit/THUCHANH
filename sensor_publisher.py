"""Mo phong cam bien gui du lieu JSON qua MQTT moi 3 giay."""

import json
import random
import time
from threading import Event

import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
DEVICE_IDS = ["sensor01", "sensor02"]
TOPIC_TEMPLATE = "iot/lab/{device_id}/data"
INTERVAL = 3


def create_sensor_data(device_id="sensor01"):
    return {
        "device_id": device_id,
        "temperature": round(random.uniform(20, 40), 1),
        "humidity": round(random.uniform(30, 80), 1),
    }


def main():
    connected = Event()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Da ket noi MQTT broker.")
            connected.set()
        else:
            print(f"Ket noi bi tu choi: {reason_code}")

    def on_disconnect(client, userdata, flags, reason_code, properties):
        connected.clear()

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    try:
        print(f"Dang ket noi {BROKER}:{PORT}...")
        client.connect(BROKER, PORT, keepalive=60)
        client.loop_start()  # Xu ly ket noi MQTT trong luong nen.
        if not connected.wait(timeout=10):
            raise RuntimeError("Khong nhan duoc xac nhan ket noi MQTT.")

        while True:
            if connected.is_set():
                for device_id in DEVICE_IDS:
                    topic = TOPIC_TEMPLATE.format(device_id=device_id)
                    payload = json.dumps(create_sensor_data(device_id))
                    result = client.publish(topic, payload, qos=0)
                    if result.rc == mqtt.MQTT_ERR_SUCCESS:
                        print(f"[{topic}] Gui: {payload}")
                    else:
                        print(f"[{device_id}] Gui that bai, ma loi: {result.rc}")
            else:
                print("Mat ket noi, dang cho ket noi lai...")
            time.sleep(INTERVAL)  # Nghi sau khi da gui du lieu cua tat ca thiet bi.
    except KeyboardInterrupt:
        print("\nDung Sensor Publisher.")
    except (OSError, RuntimeError) as error:
        print(f"Loi MQTT ({BROKER}:{PORT}): {error}")
    finally:
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    main()
