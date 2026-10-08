# Thực hành Python với giao thức MQTT

Dự án gồm 3 bài thực hành MQTT bằng Python:

- Bài 1: Publisher và Subscriber gửi/nhận thông điệp cơ bản.
- Bài 2: Mô phỏng cảm biến nhiệt độ, độ ẩm gửi dữ liệu JSON.
- Bài 3: Điều khiển đèn thông minh qua MQTT.

## 1. Yêu cầu cài đặt

Cần cài:

- Python 3.x
- Thư viện `paho-mqtt`
- Kết nối Internet để dùng MQTT broker công cộng

Kiểm tra Python:

```powershell
python --version
```

Nếu máy không nhận lệnh `python`, thử:

```powershell
py --version
```

## 2. Cài thư viện

Sau khi tải hoặc clone repository từ GitHub, mở PowerShell tại thư mục chứa code.

Ví dụ nếu đang ở thư mục cha của project:

```powershell
cd THUCHANH
```

Hoặc thay `THUCHANH` bằng tên thư mục bạn đã clone về.

Tạo môi trường ảo:

```powershell
py -m venv .venv
```

Kích hoạt môi trường ảo:

```powershell
.\.venv\Scripts\Activate.ps1
```

Cài thư viện:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

File `requirements.txt` chỉ cần thư viện:

```text
paho-mqtt>=2.1,<3
```

Kiểm tra thư viện đã cài:

```powershell
.\.venv\Scripts\python.exe -m pip show paho-mqtt
```

Lưu ý: thư mục `.venv` chỉ dùng để chạy trên máy cá nhân, không cần đưa lên GitHub.

## 3. Cấu hình MQTT broker

Các chương trình đều dùng MQTT port `1883`, không dùng username/password.

| Bài | File | Broker | Port | Topic |
| --- | --- | --- | --- | --- |
| Bài 1 | `publisher_bai1.py`, `subscriber_bai1.py` | `broker.emqx.io` | `1883` | `iot/lab/message` |
| Bài 2 | `sensor_publisher.py`, `monitoring_subscriber.py` | `broker.hivemq.com` | `1883` | `iot/lab/+/data` |
| Bài 3 | `device_bai3.py`, `controller_bai3.py` | `broker.emqx.io` | `1883` | `iot/lab/light01/cmd`, `iot/lab/light01/status` |


## 4. Chạy bài 1: Gửi và nhận thông điệp MQTT

Bài 1 dùng 2 file:

- `subscriber_bai1.py`: nhận thông điệp.
- `publisher_bai1.py`: gửi thông điệp.

### Bước 1: Chạy subscriber

Mở terminal thứ nhất:

```powershell
.\.venv\Scripts\python.exe subscriber_bai1.py
```

Subscriber sẽ kết nối broker và lắng nghe topic:

```text
iot/lab/message
```

### Bước 2: Chạy publisher

Mở terminal thứ hai:

```powershell
.\.venv\Scripts\python.exe publisher_bai1.py
```

Nhập nội dung cần gửi, ví dụ:

```text
Xin chao tu client Python MQTT
```

Publisher sẽ gửi nội dung lên MQTT broker. Payload có dạng:

```text
Xin chao tu client Python MQTT - B23DCCN004 - Nguyen Van An
```

Nhập `EXIT` để dừng publisher.

Nhấn `Ctrl+C` để dừng subscriber.

### Kết quả mong đợi

Ở terminal subscriber:

```text
Nhan duoc message
Topic: iot/lab/message
Payload: Xin chao tu client Python MQTT - B23DCCN004 - Nguyen Van An
Time: 10:15:20
```

## 5. Chạy bài 2: Mô phỏng cảm biến nhiệt độ và độ ẩm

Bài 2 dùng 2 file:

- `monitoring_subscriber.py`: nhận dữ liệu cảm biến và kiểm tra cảnh báo.
- `sensor_publisher.py`: mô phỏng cảm biến gửi dữ liệu mỗi 3 giây.

### Bước 1: Chạy monitoring subscriber

Mở terminal thứ nhất:

```powershell
.\.venv\Scripts\python.exe monitoring_subscriber.py
```

Subscriber sẽ lắng nghe topic:

```text
iot/lab/+/data
```

Ký tự `+` là wildcard, dùng để nhận dữ liệu từ nhiều thiết bị như `sensor01`, `sensor02`.

### Bước 2: Chạy sensor publisher

Mở terminal thứ hai:

```powershell
.\.venv\Scripts\python.exe sensor_publisher.py
```

Publisher sẽ gửi dữ liệu của `sensor01` và `sensor02` lên broker mỗi 3 giây.

Payload gửi đi có dạng JSON:

```json
{
  "device_id": "sensor01",
  "temperature": 28.5,
  "humidity": 65.2
}
```

### Điều kiện cảnh báo

- Nếu nhiệt độ `> 35` thì in `CANH BAO: Nhiet do cao`.
- Nếu độ ẩm `< 40` thì in `CANH BAO: Do am thap`.

Nhấn `Ctrl+C` ở mỗi terminal để dừng chương trình.

### Kết quả mong đợi

Ở terminal monitoring subscriber:

```text
Thoi gian | Thiet bi     | Nhiet do (C) | Do am (%) | Trang thai
--------------------------------------------------------------------------------------------------------------
10:20:01 | sensor01     |         36.1 |      38.7 | CANH BAO: Nhiet do cao; CANH BAO: Do am thap
10:20:01 | sensor02     |         28.5 |      65.2 | Binh thuong
```

## 6. Chạy bài 3: Điều khiển đèn thông minh

Bài 3 dùng 2 file:

- `device_bai3.py`: mô phỏng đèn thông minh `light01`.
- `controller_bai3.py`: gửi lệnh `ON`, `OFF` và nhận trạng thái phản hồi.

Hai file hiện đang dùng cùng broker:

```python
BROKER = "broker.emqx.io"
PORT = 1883
```

Topic sử dụng:

```text
iot/lab/light01/cmd
iot/lab/light01/status
```

### Bước 1: Chạy thiết bị đèn

Mở terminal thứ nhất:

```powershell
.\.venv\Scripts\python.exe device_bai3.py
```

Thiết bị sẽ lắng nghe lệnh trên topic:

```text
iot/lab/light01/cmd
```

### Bước 2: Chạy controller

Mở terminal thứ hai:

```powershell
.\.venv\Scripts\python.exe controller_bai3.py
```

Nhập một trong các lệnh:

```text
ON
OFF
EXIT
```

Ý nghĩa:

- `ON`: bật đèn.
- `OFF`: tắt đèn.
- `EXIT`: dừng controller.

Để dừng `device_bai3.py`, nhấn `Ctrl+C`.

### Kết quả mong đợi

Ở terminal controller:

```text
Nhap lenh: ON
Da gui lenh ON toi light01
Trang thai nhan duoc:
{
  "device_id": "light01",
  "status": "ON"
}
```

Ở terminal device:

```text
Received command: ON
Published status: {"device_id": "light01", "status": "ON"}
```

## 7. Lỗi thường gặp

### Không nhận lệnh `python`

Nếu PowerShell không nhận lệnh `python`, dùng:

```powershell
py -m venv .venv
```

Sau đó chạy chương trình bằng:

```powershell
.\.venv\Scripts\python.exe ten_file.py
```

### Không kết nối được broker

Kiểm tra Internet và port `1883`:

```powershell
Test-NetConnection broker.emqx.io -Port 1883
Test-NetConnection broker.hivemq.com -Port 1883
```

Nếu `TcpTestSucceeded` là `False`, mạng hiện tại có thể đang chặn kết nối MQTT port `1883`.

### Subscriber không nhận được dữ liệu

Kiểm tra:

- Đã chạy subscriber trước publisher chưa.
- Hai file trong cùng một bài có dùng cùng broker không.
- Topic publish và subscribe có khớp không.
- Máy có Internet không.

## 8. Danh sách file

| File | Mô tả |
| --- | --- |
| `publisher_bai1.py` | Publisher của bài 1 |
| `subscriber_bai1.py` | Subscriber của bài 1 |
| `sensor_publisher.py` | Sensor publisher của bài 2 |
| `monitoring_subscriber.py` | Monitoring subscriber của bài 2 |
| `device_bai3.py` | Thiết bị đèn thông minh của bài 3 |
| `controller_bai3.py` | Controller điều khiển đèn của bài 3 |
| `requirements.txt` | Danh sách thư viện cần cài |
| `TH.docx` | File đề bài thực hành |
