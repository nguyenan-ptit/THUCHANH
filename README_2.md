# Bài 2: Mô phỏng cảm biến nhiệt độ và độ ẩm bằng MQTT

Luồng dữ liệu: Sensor Publisher → MQTT broker → Monitoring Subscriber.

## Cài đặt và chạy

Mở PowerShell tại thư mục `E:\IOT-B1`, tạo môi trường và cài thư viện:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Mở terminal thứ nhất, chạy Subscriber trước:

```powershell
.\.venv\Scripts\python.exe monitoring_subscriber.py
```

Mở terminal thứ hai trong cùng thư mục, chạy Publisher:

```powershell
.\.venv\Scripts\python.exe sensor_publisher.py
```

Nhấn `Ctrl+C` ở mỗi terminal để dừng.

Hai chương trình mặc định kết nối broker công cộng `broker.hivemq.com`, cổng `1883`, nên cần Internet. Topic công cộng có thể nhận thêm dữ liệu từ người khác cùng làm bài. Nếu lớp có broker riêng, thay `BROKER` và `PORT` trong **cả hai file** bằng cùng địa chỉ và cổng của broker đó. Với broker chạy trên máy cá nhân, dùng `BROKER = "localhost"` sau khi đã khởi động broker.

Nếu gặp `Loi MQTT: timed out`, kiểm tra kết nối bằng `Test-NetConnection broker.hivemq.com -Port 1883`. Nếu `TcpTestSucceeded` là `False`, kết nối TCP đến broker không thành công; có thể do broker không phản hồi hoặc mạng chặn cổng. Thử mạng khác hoặc broker của lớp, đồng thời cập nhật cùng broker trong cả hai chương trình.

## Giải thích

- `random.uniform()` sinh nhiệt độ 20–40°C và độ ẩm 30–80%, làm tròn một chữ số thập phân.
- `json.dumps()` chuyển dữ liệu thành JSON với đúng ba trường đề bài yêu cầu.
- Một Publisher mô phỏng cả `sensor01` và `sensor02`, mỗi thiết bị có giá trị ngẫu nhiên riêng. Mỗi vòng gửi lên hai topic `iot/lab/sensor01/data` và `iot/lab/sensor02/data`, rồi nghỉ 3 giây.
- Subscriber đăng ký `iot/lab/+/data`: dấu `+` khớp một cấp tên thiết bị, nên nhận được cả hai topic. Dùng `json.loads()` để phân tích dữ liệu.
- Mỗi bản tin hiển thị trên một dòng với các cột căn lề: thời gian nhận trên máy, thiết bị, nhiệt độ, độ ẩm và trạng thái. Thời gian chỉ dùng khi hiển thị, JSON vẫn có đúng ba trường của đề bài.
- Hai câu lệnh `if` độc lập kiểm tra `temperature > 35` và `humidity < 40`. Ở đúng 35°C hoặc 40%, điều kiện tương ứng không phát cảnh báo.
- Payload sai định dạng được báo lỗi, chương trình tiếp tục nhận bản tin khác.

Ví dụ bảng kết quả (số thực tế được sinh ngẫu nhiên):

```text
Thoi gian | Thiet bi     | Nhiet do (C) | Do am (%) | Trang thai
--------------------------------------------------------------------------------------------------------------
14:30:00 | sensor01     |         36.1 |      38.7 | CANH BAO: Nhiet do cao; CANH BAO: Do am thap
14:30:00 | sensor02     |         28.5 |      65.2 | Binh thuong
14:30:03 | sensor01     |         30.2 |      55.4 | Binh thuong
14:30:03 | sensor02     |         37.0 |      60.0 | CANH BAO: Nhiet do cao
```

Để thử đúng ví dụ này, tạm thay hai biểu thức sinh ngẫu nhiên trong `create_sensor_data()` bằng `36.1` và `38.7`, rồi chạy Publisher. Khôi phục biểu thức ngẫu nhiên sau khi thử.

Để thêm thiết bị, bổ sung tên vào `DEVICE_IDS` trong `sensor_publisher.py`, ví dụ `DEVICE_IDS = ["sensor01", "sensor02", "sensor03"]`. Subscriber tự nhận thiết bị mới, không cần sửa. Chỉ dùng tên thiết bị đơn giản, không chứa `/`, `+` hoặc `#`.

Tham khảo API thư viện: [Eclipse Paho MQTT Python](https://eclipse.dev/paho/clients/python/docs/).
