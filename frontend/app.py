import streamlit as st
from collections import deque
from datetime import date
import requests
import pandas as pd

#from api_client import signup, login, google_login, get_messages, send_chat
from api_client import signup, login, google_login, create_expense, get_expenses

st.set_page_config(page_title="Ứng Dụng Quản Lý Chi Tiêu", page_icon="🤑")

st.title("Ứng Dụng Quản Lý Chi Tiêu 🏧")

# ================== STATE ==================
if "user" not in st.session_state:
    st.session_state.user = None

if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

if "expenses" not in st.session_state:
    st.session_state.expenses = []

# ================== HELPER ==================
def load_expenses():
    try:
        data = get_expenses(st.session_state.user["idToken"])
        st.session_state.expenses = data
    except Exception as e:
        st.error(f"Lỗi load dữ liệu: {e}")
        st.session_state.expenses = []

def clear_google_query_params():
    try:
        st.query_params.clear()
    except:
        pass

def handle_google_login_callback():
    if st.session_state.user:
        return

    params = st.query_params
    raw_token = params.get("id_token")

    if not raw_token:
        return

    id_token = raw_token[0] if isinstance(raw_token, list) else raw_token

    try:
        user = google_login(id_token)
        st.session_state.user = user
        load_expenses()
        clear_google_query_params()
        st.success("Đăng nhập Google thành công")
        st.rerun()
    except Exception as e:
        st.error(f"Google login lỗi: {e}")
        clear_google_query_params()

# ================== AUTH ==================
def login_form():
    st.subheader("Đăng nhập")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        login_btn = st.form_submit_button("Đăng nhập")
        signup_btn = st.form_submit_button("Chưa có tài khoản?")

    if signup_btn:
        st.session_state.show_signup = True
        st.rerun()

    if login_btn:
        try:
            user = login(email, password)
            st.session_state.user = user
            load_expenses()
            st.success("Đăng nhập thành công")
            st.rerun()
        except Exception as e:
            st.error(f"Lỗi đăng nhập: {e}")

    st.markdown("### Hoặc")

    google_url = dict(st.secrets["google-login"])["google-url"]
    if google_url:
        st.markdown(f'<a href="{google_url}">Đăng nhập với Google</a>', unsafe_allow_html=True)

def signup_form():
    st.subheader("Đăng ký")

    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        submit = st.form_submit_button("Tạo tài khoản")
        back = st.form_submit_button("Quay lại đăng nhập")

    if back:
        st.session_state.show_signup = False
        st.rerun()

    if submit:
        try:
            signup(email, password)
            st.success("Tạo tài khoản thành công")
            st.session_state.show_signup = False
            st.rerun()
        except Exception as e:
            st.error(f"Lỗi đăng ký: {e}")
    
# ================== MAIN ==================
handle_google_login_callback()

if st.session_state.user:

    st.success(f"Xin chào: {st.session_state.user['email']}")

    if st.button("Đăng xuất"):
        st.session_state.user = None
        st.session_state.expenses = []
        clear_google_query_params()
        st.rerun()

    st.divider()

    tab1, tab2 = st.tabs(["➕ Nhập chi tiêu", "📊 Thống kê"])

    # ================== TAB 1 ==================
    with tab1:
        st.subheader("Thêm chi tiêu")

        with st.form("expense_form"):
            col1, col2 = st.columns(2)

            with col1:
                ngay = st.date_input("Ngày", value=date.today())
                category = st.selectbox("Danh mục", ["Ăn uống", "Di chuyển", "Mua sắm", "Khác"])

            with col2:
                note = st.text_input("Ghi chú")
                amount = st.number_input("Số tiền (VNĐ)", min_value=0)

            submit = st.form_submit_button("Lưu")

            if submit:
                try:
                    create_expense(
                        st.session_state.user["idToken"],
                        {
                            "amount": amount,
                            "category": category,
                            "note": note
                        }
                    )
                    st.success("Đã lưu vào database!")
                    load_expenses()
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi lưu: {e}")

    # ================== TAB 2 ==================
    with tab2:
        st.subheader("Thống kê chi tiêu")

        if st.session_state.expenses:
            df = pd.DataFrame(st.session_state.expenses)

            total = df["amount"].sum()
            st.metric("💸 Tổng chi", f"{total:,.0f} VNĐ")

            df["amount"] = df["amount"].apply(lambda x: f"{x:,.0f} đ")

            st.dataframe(df, use_container_width=True, hide_index=True)

        else:
            st.info("Chưa có dữ liệu")

else:
    if st.session_state.show_signup:
        signup_form()
    else:
        login_form()

# st.markdown("""
# <style>
#     /* Nền trắng */
#     .stApp {
#         background-color: white;
#         color: black;
#     }

#     /* Text chung */
#     html, body, [class*="css"]  {
#         color: black !important;
#     }

#     /* Ô input */
#     .stTextInput input {
#         background-color: white !important;
#         color: black !important;
#         border: 1px solid #1d4ed8 !important; /* xanh */
#         border-radius: 10px;
#     }

#     /* Placeholder */
#     ::placeholder {
#         color: #6b7280 !important;
#     }

#     /* Button chung */
#     button {
#         border-radius: 10px !important;
#         background-color: #55a845 !important; /* xanh nước biển */
#         color: white !important;
#         border: none !important;
#         font-weight: 600;
#     }

#     /* Hover */
#     button:hover {
#         background-color: #1e40af !important;
#     }

#     /* Nút Google (link <a>) */
#     a {
#         background-color:  #55a845 !important;
#         color: white !important;
#         border-radius: 10px !important;
#         display: inline-block;
#         text-align: center;
#         padding: 0.6rem 1rem;
#         font-weight: 600;
#         border: none !important;
#     }

#     a:hover {
#         background-color: #1e40af !important;
#         color: white !important;
#     }

#     /* Form box */
#     .stForm {
#         background-color: white !important;
#         border: 1px solid #e5e7eb;
#         padding: 20px;
#         border-radius: 12px;
#     }
# </style>
# """, unsafe_allow_html=True)

# WELCOME = {"role": "assistant", "content": "Xin chào 👋! Tôi là Mika. Tôi có thể giúp gì cho bạn?"}

# if "user" not in st.session_state:
#     st.session_state.user = None

# if "messages" not in st.session_state:
#     st.session_state.messages = deque([WELCOME], maxlen=8)

# if "show_signup" not in st.session_state:
#     st.session_state.show_signup = False

# if "show_login" not in st.session_state:
#     st.session_state.show_login = True

# if "chi_tieu_list" not in st.session_state:
#     st.session_state.chi_tieu_list = []

# if "thu_nhap_list" not in st.session_state:
#     st.session_state.thu_nhap_list = []


# def load_history():
#     if not st.session_state.user:
#         return
#     try:
#         msgs = get_messages(st.session_state.user["idToken"], limit=8)
#         st.session_state.messages = deque(msgs, maxlen=8)
#     except Exception:
#         st.session_state.messages = deque([WELCOME], maxlen=8)


# def clear_google_query_params():
#     try:
#         st.query_params.clear()
#     except Exception:
#         pass


# def handle_google_login_callback():
#     if st.session_state.user:
#         return

#     params = st.query_params
#     raw_token = params.get("id_token")

#     if not raw_token:
#         return

#     id_token = raw_token[0] if isinstance(raw_token, list) else raw_token

#     try:
#         user = google_login(id_token)
#         st.session_state.user = user
#         load_history()
#         clear_google_query_params()
#         st.success("Đăng nhập Google thành công")
#         st.rerun()
#     except requests.HTTPError as e:
#         st.error(f"Đăng nhập Google thất bại: {e}")
#         clear_google_query_params()
#     except Exception as e:
#         st.error(f"Lỗi xử lý Google login: {e}")
#         clear_google_query_params()


# def login_form():
#     st.subheader("Đăng nhập")

#     with st.form("login_form"):
#         email = st.text_input("Email")
#         password = st.text_input("Mật khẩu", type="password")
#         submitted = st.form_submit_button("Đăng nhập")
#         goto_signup = st.form_submit_button("Chưa có tài khoản? Đăng ký")

#     if goto_signup:
#         st.session_state.show_signup = True
#         st.session_state.show_login = False
#         st.rerun()

#     if submitted:
#         try:
#             user = login(email, password)
#             st.session_state.user = user
#             load_history()
#             st.success("Đăng nhập thành công")
#             st.rerun()
#         except requests.HTTPError as e:
#             st.error(f"Đăng nhập thất bại: {e}")
#         except Exception as e:
#             st.error(f"Lỗi đăng nhập: {e}")

#     st.markdown("### Hoặc")

#     google_login_url = dict(st.secrets["google-login"])["google-url"]

#     if google_login_url:
#         st.markdown(
#         f'''
#         <a href="{google_login_url}" target="_self" style="
#             display: inline-block;
#             width: 100%;
#             text-align: center;
#             padding: 0.6rem 1rem;
#             background-color: white;
#             color: black;
#             text-decoration: none;
#             border-radius: 0.5rem;
#             border: 1px solid #ddd;
#             font-weight: 600;
#         ">
#             Đăng nhập với Google
#         </a>
#         ''',
#         unsafe_allow_html=True,
#     )
#     else:
#         st.info(
#             "Chưa cấu hình Google-login trong secrets. "
#             "Hãy thêm URL đăng nhập Google để dùng tính năng này."
#         )


# def signup_form():
#     st.subheader("Đăng ký")
#     with st.form("signup_form"):
#         email = st.text_input("Email")
#         password = st.text_input("Mật khẩu", type="password")
#         submitted = st.form_submit_button("Tạo tài khoản")
#         goto_login = st.form_submit_button("Đã có tài khoản? Đăng nhập")

#     if goto_login:
#         st.session_state.show_signup = False
#         st.session_state.show_login = True
#         st.rerun()

#     if submitted:
#         try:
#             signup(email, password)
#             st.success("Tạo tài khoản thành công, hãy đăng nhập")
#             st.session_state.show_signup = False
#             st.session_state.show_login = True
#             st.rerun()
#         except requests.HTTPError as e:
#             error_text = str(e)
#             if e.response is not None:
#                 try:
#                     payload = e.response.json()
#                     detail = payload.get("detail")
#                     if detail:
#                         error_text = f"{e} - {detail}"
#                 except ValueError:
#                     # Keep original HTTPError text if response is not JSON.
#                     pass
#             st.error(f"Đăng ký thất bại: {error_text}")
#         except Exception as e:
#             st.error(f"Lỗi đăng ký: {e}")


# handle_google_login_callback()

# # if st.session_state.user:
# #     st.success(f"Đang đăng nhập: {st.session_state.user['email']}")
# #     if st.button("Đăng xuất"):
# #         st.session_state.user = None
# #         st.session_state.messages = deque([WELCOME], maxlen=8)
# #         clear_google_query_params()
# #         st.rerun()
# # else:
# #     if st.session_state.show_signup:
# #         signup_form()
# #     else:
# #         login_form()

# # st.divider()

# # if st.session_state.user:
# #     for msg in list(st.session_state.messages):
# #         with st.chat_message(msg["role"]):
# #             st.markdown(msg["content"])

# #     prompt = st.chat_input("Nhập tin nhắn...")
# #     if prompt:
# #         st.session_state.messages.append({"role": "user", "content": prompt})
# #         with st.chat_message("user"):
# #             st.markdown(prompt)

# #         try:
# #             res = send_chat(st.session_state.user["idToken"], prompt)
# #             reply = res["reply"]
# #         except Exception as e:
# #             reply = f"Lỗi backend: {e}"

# #         st.session_state.messages.append({"role": "assistant", "content": reply})
# #         st.rerun()

# if st.session_state.user:
#     st.success(f"Xin chào: {st.session_state.user['email']}")

#     if st.button("Đăng xuất"):
#         st.session_state.user = None
#         st.session_state.messages = deque([WELCOME], maxlen=8)
#         clear_google_query_params()
#         st.rerun()

#     st.divider()

#     # 👉 UI quản lý chi tiêu
#     # st.header("💰 Quản lý chi tiêu")

#     # amount = st.number_input("Số tiền", min_value=0)
#     # category = st.selectbox("Danh mục", ["Ăn uống", "Đi lại", "Mua sắm"])
#     # note = st.text_input("Ghi chú")

#     # if st.button("Lưu"):
#     #     st.success("Đã lưu!")

#     # st.divider()

#     # st.subheader("📋 Danh sách chi tiêu")

#     # data = [
#     #     {"Số tiền": 50000, "Danh mục": "Ăn uống"},
#     #     {"Số tiền": 20000, "Danh mục": "Đi lại"}
#     # ]

#     st.markdown("""
#     <style>
#     /* Nền tổng */
#     .stApp {
#         background-color: white;
#     }

#     /* Text toàn bộ */
#     html, body, [class*="css"] {
#         color: black !important;
#     }

#     /* Input */
#     input, textarea {
#         background-color: white !important;
#         color: black !important;
#         border: 1px solid #ccc !important;
#         border-radius: 8px !important;
#     }

#     /* Selectbox */
#     div[data-baseweb="select"],
#     div[data-baseweb="select"] > div {
#         background-color: white !important;
#         color: black !important;
#     }

#     /* Dropdown list khi mở */
#     ul[data-baseweb="menu"],
#     li[data-baseweb="menu-item"] {
#         background-color: white !important;
#         color: black !important;
#     }

#     li[data-baseweb="menu-item"]:hover {
#         background-color: #f0fdf4 !important;
#     }

#     /* Success message - giống nút Lưu */
#     [data-testid="stAlert"][data-baseweb="notification"],
#     div[data-testid="stAlert"] {
#         background-color: #22c55e !important;
#         color: white !important;
#         border-radius: 8px !important;
#         border: none !important;
#         font-weight: 600 !important;
#     }

#     [data-testid="stAlert"] p,
#     [data-testid="stAlert"] span,
#     [data-testid="stAlert"] svg {
#         color: white !important;
#         fill: white !important;
#     }

#     /* Number input */
#     div[data-baseweb="input"] {
#         background-color: white !important;
#     }

#     /* Date input */
#     input[type="date"] {
#         background-color: white !important;
#         color: black !important;
#     }

#     /* Form box */
#     .stForm {
#         background-color: white !important;
#         border: 1px solid #ddd;
#         border-radius: 12px;
#         padding: 20px;
#     }

#     /* Button */
#     button {
#         background-color: #22c55e !important;
#         color: white !important;
#         border-radius: 8px !important;
#         border: none !important;
#     }

#     button:hover {
#         background-color: #16a34a !important;
#     }

#     /* XÓA cảnh báo màu hồng */
#     [data-testid="stForm"] > div {
#         background-color: white !important;
#     }

#     /* Fix label màu đen */
#     label, .stTextInput label, .stNumberInput label,
#     .stSelectbox label, .stDateInput label,
#     [data-testid="stWidgetLabel"] p,
#     [data-testid="stWidgetLabel"] {
#         color: black !important;
#     }

#     /* Fix metric màu đen */
#     [data-testid="stMetric"] label,
#     [data-testid="stMetricLabel"] p,
#     [data-testid="stMetricValue"] p,
#     [data-testid="stMetricValue"],
#     [data-testid="stMetricLabel"] {
#         color: black !important;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     # st.table(data)
#     tab1, tab2, tab3 = st.tabs(["Chi Tiêu", "Thu Nhập", "Quản lý"])

#     with tab1:
#         st.header("Nhập chi tiêu")
#         with st.form("expense_form_1"):
#             col1, col2 = st.columns(2)
#             with col1:
#                 ngay = st.date_input("Ngày", value = date.today())
#                 loai = st.selectbox("Loại chi tiêu", ["Ăn uống", "Di chuyển", "Mua sắm", "Khác"])
#             with col2:
#                 ten = st.text_input("Tên mục chi")
#                 soten = st.number_input("Số tiền(VNĐ)", min_value = 0)
#             submit = st.form_submit_button("Lưu chi tiêu")

#             if submit:
#                 st.session_state.chi_tieu_list.append({
#                     "Ngày": str(ngay),
#                     "Tên mục chi": ten,
#                     "Loại": loai,
#                     "Số tiền (VNĐ)": soten,
#                 })
#                 st.success("Đã lưu chi tiêu!")
       
#     with tab2:
#         st.header("Nhập thu nhập")
#         with st.form("expense_form_2"):
#             col1, col2 = st.columns(2)
#             with col1:
#                 ngay = st.date_input("Ngày", value = date.today())
#                 loai = st.selectbox("Loại thu nhập", ["Lương", "Gửi tiết kiệm", "Khác"])
#             with col2:
#                 ten = st.text_input("Tên thu nhập")
#                 soten = st.number_input("Số tiền(VNĐ)", min_value = 0)

#             submit = st.form_submit_button("Lưu thu nhập")

#             if submit:
#                 st.session_state.thu_nhap_list.append({
#                     "Ngày": str(ngay),
#                     "Tên thu nhập": ten,
#                     "Loại": loai,
#                     "Số tiền (VNĐ)": soten,
#                 })
#                 st.success("Đã lưu thu nhập!")
        
#     with tab3:
#         st.header("Danh sách quản lý chi tiêu")

#         tong_chi = sum(item["Số tiền (VNĐ)"] for item in st.session_state.chi_tieu_list)
#         tong_thu = sum(item["Số tiền (VNĐ)"] for item in st.session_state.thu_nhap_list)
#         con_lai = tong_thu - tong_chi

#         col1, col2, col3 = st.columns(3)
#         col1.metric("💸 Tổng chi", f"{tong_chi:,.0f} đ")
#         col2.metric("💰 Tổng thu", f"{tong_thu:,.0f} đ")
#         col3.metric("🏦 Còn lại", f"{con_lai:,.0f} đ", delta=None)

#         st.divider()

#         st.subheader("📋 Chi tiêu")
#         if st.session_state.chi_tieu_list:
#             import pandas as pd
#             df_chi = pd.DataFrame(st.session_state.chi_tieu_list)
#             df_chi["Số tiền (VNĐ)"] = df_chi["Số tiền (VNĐ)"].apply(lambda x: f"{x:,.0f} đ")
#             st.dataframe(df_chi, use_container_width=True, hide_index=True)
#             if st.button("🗑️ Xóa toàn bộ chi tiêu"):
#                 st.session_state.chi_tieu_list = []
#                 st.rerun()
#         else:
#             st.info("Chưa có dữ liệu chi tiêu.")

#         st.divider()

#         st.subheader("📋 Thu nhập")
#         if st.session_state.thu_nhap_list:
#             import pandas as pd
#             df_thu = pd.DataFrame(st.session_state.thu_nhap_list)
#             df_thu["Số tiền (VNĐ)"] = df_thu["Số tiền (VNĐ)"].apply(lambda x: f"{x:,.0f} đ")
#             st.dataframe(df_thu, use_container_width=True, hide_index=True)
#             if st.button("🗑️ Xóa toàn bộ thu nhập"):
#                 st.session_state.thu_nhap_list = []
#                 st.rerun()
#         else:
#             st.info("Chưa có dữ liệu thu nhập.")


# else:
#     if st.session_state.show_signup:
#         signup_form()
#     else:
#         login_form()