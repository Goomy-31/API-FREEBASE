import streamlit as st
import pandas as pd
from datetime import date

from api_client import signup, login, google_login, create_expense, get_expenses

st.set_page_config(page_title="Quản Lý Chi Tiêu", page_icon="🤑", layout="centered")

st.title("Ứng Dụng Quản Lý Chi Tiêu 🏧")

# ================== SESSION STATE ==================
if "user" not in st.session_state:
    st.session_state.user = None

if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

if "expenses" not in st.session_state:
    st.session_state.expenses = []


# ================== HELPER ==================
def load_expenses():
    try:
        # FIX: Backend trả về idToken trong response login
        data = get_expenses(st.session_state.user["idToken"])
        st.session_state.expenses = data
    except Exception as e:
        st.error(f"Lỗi load dữ liệu: {e}")
        st.session_state.expenses = []


def clear_google_query_params():
    try:
        st.query_params.clear()
    except Exception:
        pass


# ================== GOOGLE CALLBACK ==================
def handle_google_login_callback():
    if st.session_state.user:
        return

    params = st.query_params
    raw_token = params.get("id_token")
    if not raw_token:
        return

    id_token = raw_token[0] if isinstance(raw_token, list) else raw_token

    try:
        # FIX: google_login trả về {"email", "uid", "idToken"}
        # Backend /auth/google trả về idToken (Firebase idToken)
        user = google_login(id_token)
        st.session_state.user = user
        load_expenses()
        clear_google_query_params()
        st.success("Đăng nhập Google thành công!")
        st.rerun()
    except Exception as e:
        st.error(f"Google login lỗi: {e}")
        clear_google_query_params()


# ================== AUTH FORMS ==================
def login_form():
    st.subheader("Đăng nhập")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.form_submit_button("Đăng nhập", use_container_width=True)
        with col2:
            signup_btn = st.form_submit_button("Tạo tài khoản", use_container_width=True)

    if signup_btn:
        st.session_state.show_signup = True
        st.rerun()

    if login_btn:
        if not email or not password:
            st.warning("Vui lòng nhập đầy đủ email và mật khẩu.")
        else:
            try:
                # FIX: Backend /auth/login trả về {"email", "uid", "idToken", "refreshToken"}
                user = login(email, password)
                st.session_state.user = user
                load_expenses()
                st.success("Đăng nhập thành công!")
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi đăng nhập: {e}")

    st.markdown("---")

    # FIX: Lấy google-url từ secrets để redirect sang /auth/google/start
    try:
        google_url = dict(st.secrets["google-login"])["google-url"]
        st.markdown(
            f'''
            <a href="{google_url}" target="_self" style="
                display: inline-block;
                width: 100%;
                text-align: center;
                padding: 0.6rem 1rem;
                background-color: #4285F4;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 15px;
            ">
                🔵 Đăng nhập với Google
            </a>
            ''',
            unsafe_allow_html=True
        )
    except Exception:
        st.info("Chưa cấu hình Google login trong secrets.")


def signup_form():
    st.subheader("Tạo tài khoản mới")

    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Tạo tài khoản", use_container_width=True)
        with col2:
            back = st.form_submit_button("Quay lại đăng nhập", use_container_width=True)

    if back:
        st.session_state.show_signup = False
        st.rerun()

    if submit:
        if not email or not password:
            st.warning("Vui lòng nhập đầy đủ thông tin.")
        else:
            try:
                signup(email, password)
                st.success("Tạo tài khoản thành công! Hãy đăng nhập.")
                st.session_state.show_signup = False
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi đăng ký: {e}")


# ================== MAIN APP ==================
handle_google_login_callback()

if st.session_state.user:
    user = st.session_state.user

    col1, col2 = st.columns([3, 1])
    with col1:
        st.success(f"👋 Xin chào: **{user['email']}**")
    with col2:
        if st.button("Đăng xuất", use_container_width=True):
            st.session_state.user = None
            st.session_state.expenses = []
            clear_google_query_params()
            st.rerun()

    st.divider()

    tab1, tab2 = st.tabs(["➕ Nhập chi tiêu", "📊 Thống kê"])

    # ================== TAB 1: NHẬP CHI TIÊU ==================
    with tab1:
        st.subheader("Thêm chi tiêu mới")

        with st.form("expense_form"):
            col1, col2 = st.columns(2)

            with col1:
                ngay = st.date_input("Ngày", value=date.today())
                # FIX: Đồng bộ với schema backend - field tên là "category"
                category = st.selectbox(
                    "Danh mục",
                    ["Ăn uống", "Di chuyển", "Mua sắm", "Giải trí", "Sức khoẻ", "Khác"]
                )

            with col2:
                # FIX: field tên là "note" (optional theo schema)
                note = st.text_input("Ghi chú (tuỳ chọn)")
                # FIX: field tên là "amount" (float theo schema)
                amount = st.number_input("Số tiền (VNĐ)", min_value=0, step=1000)

            submit = st.form_submit_button("💾 Lưu chi tiêu", use_container_width=True)

        if submit:
            if amount <= 0:
                st.warning("Vui lòng nhập số tiền lớn hơn 0.")
            else:
                try:
                    create_expense(
                        user["idToken"],
                        {
                            "amount": float(amount),
                            "category": category,
                            "note": note if note else None  # FIX: note optional, gửi None nếu trống
                        }
                    )
                    st.success("✅ Đã lưu chi tiêu!")
                    load_expenses()
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi lưu: {e}")

    # ================== TAB 2: THỐNG KÊ ==================
    with tab2:
        st.subheader("Thống kê chi tiêu")

        if st.button("🔄 Tải lại dữ liệu"):
            load_expenses()
            st.rerun()

        expenses = st.session_state.expenses

        if expenses:
            df = pd.DataFrame(expenses)

            # Metrics
            total = df["amount"].sum()
            count = len(df)
            avg = total / count if count > 0 else 0

            col1, col2, col3 = st.columns(3)
            col1.metric("💸 Tổng chi", f"{total:,.0f} đ")
            col2.metric("📋 Số giao dịch", count)
            col3.metric("📊 Trung bình", f"{avg:,.0f} đ")

            st.divider()

            # FIX: Hiển thị đúng các field trả về từ backend
            # Backend trả về: id, amount, category, note, created_at
            display_df = df.copy()

            # Format cột hiển thị
            display_df = display_df.rename(columns={
                "amount": "Số tiền",
                "category": "Danh mục",
                "note": "Ghi chú",
                "created_at": "Thời gian",
                "id": "ID"
            })

            # Format số tiền
            display_df["Số tiền"] = display_df["Số tiền"].apply(lambda x: f"{x:,.0f} đ")

            # Chỉ hiển thị các cột cần thiết, bỏ ID
            cols_show = ["Danh mục", "Số tiền", "Ghi chú", "Thời gian"]
            cols_available = [c for c in cols_show if c in display_df.columns]

            st.dataframe(display_df[cols_available], use_container_width=True, hide_index=True)

            # Biểu đồ theo danh mục
            st.divider()
            st.subheader("Chi tiêu theo danh mục")
            chart_df = df.groupby("category")["amount"].sum().reset_index()
            chart_df.columns = ["Danh mục", "Tổng tiền"]
            st.bar_chart(chart_df.set_index("Danh mục"))

        else:
            st.info("Chưa có dữ liệu chi tiêu nào.")

else:
    if st.session_state.show_signup:
        signup_form()
    else:
        login_form()