import paho.mqtt.client as mqtt

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "iot/lab/message"

ho_ten = "Nguyen Van An"
ma_sinh_vien = "B23DCCN004"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect(BROKER, PORT, 60)

print("Ket noi MQTT broker thanh cong")
print("Nhap EXIT de dung chuong trinh.")

while True:
    noi_dung = input("\nNhap noi dung muon gui: ")

    if noi_dung.upper() == "EXIT":
        break

    message = f"{noi_dung} - {ma_sinh_vien} - {ho_ten}"

    result = client.publish(TOPIC, message)
    result.wait_for_publish()

client.disconnect()
print("Da dung Publisher.")