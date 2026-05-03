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
``` bash
   [firebase_client]
   apiKey = "YOUR_FIREBASE_WEB_API_KEY"
   authDomain = "YOUR_PROJECT.firebaseapp.com"
   projectId = "YOUR_PROJECT_ID"
   storageBucket = "YOUR_PROJECT.appspot.com"
   messagingSenderId = "YOUR_SENDER_ID"
   appId = "YOUR_APP_ID"
   
   [firebase_admin]
   type = "service_account"
   project_id = "YOUR_PROJECT_ID"
   private_key_id = "YOUR_PRIVATE_KEY_ID"
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   client_email = "firebase-adminsdk-xxx@YOUR_PROJECT_ID.iam.gserviceaccount.com"
   client_id = "YOUR_CLIENT_ID"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "YOUR_CLIENT_X509_CERT_URL"
   universe_domain = "googleapis.com"
   
   [google-login]
   frontend_url = "http://localhost:8501"
   google_client_id = "YOUR_GOOGLE_CLIENT_ID"
   google_client_secret = "YOUR_GOOGLE_CLIENT_SECRET"
   google_redirect_uri = "http://localhost:8501"
   google_scopes = "openid email profile"
   cors_origins = "http://localhost:8501"
   ```

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
https://github.com/user-attachments/assets/79190465-fcca-4388-8af8-3c233df6f57f
