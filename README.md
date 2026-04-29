# 📝 Lab 2: API-Firebase/ Ứng dụng quản lý chi tiêu
### Thông tin sinh viên
* ### Họ và Tên: Võ Văn Khánh Đăng
* ### MSSV: 24120278
* ### Lớp: 24CTT3


* ### Đây là ứứng dụng quản lý chi tiêu của người dùng theo tháng

## 🛠️ Hướng dẫn cài đặt Environment

1. Clone dự án:
   ```bash
   git clone https://github.com/Ponnef/Lab2_API_Firebase_NoteApp
   cd Lab2_API_Firebase_NoteApp
   ```

2. Cài đặt thư viện:
   ``` bash
   pip install -r requirements.txt
   ```

## Hướng dẫn chạy Backend
1. Đảm bảo bạn đã có file `backend/serviceAccountKey.json` từ Firebase Console

2. Di chuyển đến thư mục backend:
   ```bash
   cd backend
   ```
3. **Khởi chạy Server:**
   ```bash
   uvicorn app.main:app --reload
   ```
## Hướng dẫn chạy Frontend

1. Đảm bảo có file `frontend/.streamlit/secrets.toml` đã được cấu hình đầy đủ Client ID và API Key.

2. **Di chuyển đến thư mục frontend:**
   ```bash
   cd frontend
   ```
3. **Khởi chạy ứng dụng:**
   ```bash
   streamlit run app.py
   ```
Ứng dụng sẽ tự động mở trên trình duyệt tại: http://localhost:8501

### **🎥 Video demo