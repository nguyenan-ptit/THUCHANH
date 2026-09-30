"""Nhan du lieu cam bien va canh bao khi vuot nguong."""

import json
import math
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "iot/lab/+/data"  # Dau + khop voi mot cap topic: sensor01, sensor02, ...


def print_table_header():
    print(f"{'Thoi gian':<8} | {'Thiet bi':<12} | {'Nhiet do (C)':>12} | {'Do am (%)':>9} | Trang thai")
    print("-" * 110)


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        # Dang ky lai ca khi client tu dong ket noi lai.
        client.subscribe(TOPIC)
        print(f"Da ket noi. Dang lang nghe topic: {TOPIC}")
        print_table_header()
    else:
        print(f"Ket noi bi tu choi: {reason_code}")


def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Payload phai la mot JSON object.")
        device_id = data["device_id"]
        temperature = data["temperature"]
        humidity = data["humidity"]
        if not isinstance(device_id, str) or not device_id:
            raise ValueError("device_id phai la chuoi khong rong.")
        for value in (temperature, humidity):
            if type(value) not in (int, float) or not math.isfinite(value):
                raise ValueError("Nhiet do va do am phai la so huu han.")

        # Hai dieu kien doc lap de co the hien ca hai canh bao.
        warnings = []
        if temperature > 35:
            warnings.append("CANH BAO: Nhiet do cao")
        if humidity < 40:
            warnings.append("CANH BAO: Do am thap")
        status = "; ".join(warnings) if warnings else "Binh thuong"
        received_at = datetime.now().strftime("%H:%M:%S")
        print(
            f"{received_at} | {device_id:<12} | {temperature:>12.1f} | "
            f"{humidity:>9.1f} | {status}",
            flush=True,
        )
    except (ValueError, KeyError, TypeError, OverflowError) as error:
        print(f"Du lieu khong hop le: {error}")


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        print(f"Dang ket noi {BROKER}:{PORT}...")
        client.connect(BROKER, PORT, keepalive=60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nDung Monitoring Subscriber.")
    except OSError as error:
        print(f"Loi MQTT ({BROKER}:{PORT}): {error}")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
