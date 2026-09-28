BÀI 1 - ỨNG DỤNG GỬI VÀ NHẬN THÔNG ĐIỆP MQTT CƠ BẢN

1. Broker sử dụng

- MQTT Broker: broker.emqx.io
- Port: 1883
- Topic: iot/lab/message
- Username: Không sử dụng
- Password: Không sử dụng

2. Các file chương trình

- publisher_bai1.py
  + Kết nối tới MQTT Broker.
  + Gửi thông điệp lên topic iot/lab/message.
  + Nội dung thông điệp gồm: nội dung chào mừng, mã sinh viên và họ tên sinh viên.
  + Có thể gửi nhiều thông điệp liên tiếp.
  + Nhập EXIT để dừng chương trình.

- subscriber_bai1.py
  + Kết nối tới cùng MQTT Broker.
  + Subscribe topic iot/lab/message.
  + Khi nhận được thông điệp, hiển thị:
    - Topic
    - Payload
    - Thời gian nhận
  + Chương trình chạy liên tục cho đến khi nhấn Ctrl+C.

3. Cách cài đặt

Cài đặt Python 3 và thư viện paho-mqtt:

pip install paho-mqtt

4. Cách chạy chương trình

Bước 1: Mở Terminal thứ nhất và chạy Subscriber:

python subscriber_bai1.py

Subscriber sẽ kết nối tới Broker và lắng nghe topic:

iot/lab/message

Bước 2: Mở Terminal thứ hai và chạy Publisher:

python publisher_bai1.py

Nhập nội dung cần gửi. Publisher sẽ gửi thông điệp lên MQTT Broker.

Ví dụ:

Nhập nội dung muốn gửi: Xin chao tu client Python MQTT

Nếu muốn kết thúc Publisher, nhập:

EXIT

Nếu muốn kết thúc Subscriber, nhấn:

Ctrl+C

5. Kết quả đạt được

- Publisher kết nối thành công tới MQTT Broker.
- Publisher gửi được thông điệp lên topic iot/lab/message.
- Subscriber subscribe và nhận được thông điệp từ Publisher.
- Subscriber hiển thị đúng Topic, Payload và thời gian nhận.
- Publisher có thể gửi nhiều thông điệp liên tiếp.
- Subscriber có thể chạy liên tục để nhận các thông điệp mới.

Ví dụ kết quả:

Nhan duoc message:
Topic: iot/lab/message
Payload: Xin chao tu client Python MQTT - B23DCCN004 - Nguyễn Văn An
Time: 23:35:20