# 📝 Lab 2: API-Firebase/ Ứng dụng quản lý chi tiêu
## 🪪 Thông tin sinh viên
* ### Họ và Tên: Võ Văn Khánh Đăng
* ### MSSV: 24120278
* ### Lớp: 24CTT3


* ### Đây là ứng dụng quản lý chi tiêu của người dùng theo tháng

## 🛠️ Hướng dẫn cài đặt Environment

1. Clone dự án:
   ```bash
   git clone https://github.com/Goomy-31/API-FREEBASE
   cd API-FREEBASE
   ```

2. Cài đặt thư viện:
   ``` bash
   pip install -r requirements.txt
   ```
## 📑 Yêu cầu trước khi chạy 
1. Tạo thư mục .Streamlit trong thư muc API-FREEBASE vừa clone về

2. Tạo file secret.toml và thêm key các từ Firebase vào

## Hướng dẫn chạy Backend
1. Mở terminal
   
2. Chạy dòng lệnh 
   ```bash
   python -m uvicorn backend.app.main:app --reload --port 8000
   ```
## Hướng dẫn chạy Frontend

1. Mở một terminal khác 
   
2. Chạy dòng lệnh 
   ```bash
   python -m streamlit run frontend/app.py
   ```

3. Ứng dụng sẽ tự động mở trên trình duyệt tại: http://localhost:8501

### **🎥 Video demo