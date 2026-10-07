import calendar
import datetime
import os
import pandas as pd
import streamlit as st

# Cấu hình giao diện
st.set_page_config(
    page_title="HongNhungTN - Quản Lý Công Việc & KPI",
    page_icon="🏆",
    layout="wide",
)

# 1. Danh sách nhân sự chính thức của công ty
DANH_SACH_NHAN_SU_CHINH_THUC = [
    "Trương Văn Thi (Giám Đốc - Mr. Thi)",
    (
        "Đặng Thị Hồng Nhung (P.Giám Đốc kiêm Trưởng Phòng Kinh Doanh -"
        " Mrs. Nhung)"
    ),
    "Hồ Ngọc Tú (Kế Toán)",
    "Lê Hoàn (Lái xe điều phối)",
    "Hồ Thậm Hải (Thiết kế ra file CNC)",
    "Đào Minh Mẫn (Phụ trách đứng máy CNC)",
    "Trương Thất Lập (Nhân viên kỹ thuật)",
    "Nông Trọng Huấn (Nhân viên kỹ thuật)",
    "Lê Thanh Hiền (Nhân viên kỹ thuật)",
    "Lê Gia Huy (Nhân viên kỹ thuật)",
    "Khúc Gia Bảo (Nhân viên kỹ thuật)",
    "Đội trần tường 1 (Lập + Huy)",
    "Đội trần tường 2 (Huấn + Bảo)",
    "Đội lắp đặt 1 (Hiền + Bảo)",
    "Đội lắp đặt 2 (Hải + Mẫn)",
    "Đội lắp đặt 3 tăng cường (Huấn + Huy + Lập)",
]

# Sử dụng tệp tạm thời chia sẻ trạng thái online giữa các phiên đám mây
ONLINE_STATE_FILE = "company_active_members.json"


def doc_trang_thai_online():
    import json

    if os.path.exists(ONLINE_STATE_FILE):
        try:
            with open(ONLINE_STATE_FILE, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                res = {}
                now = datetime.datetime.now()
                for k, v in raw_data.items():
                    t = datetime.datetime.fromisoformat(v)
                    if (now - t).total_seconds() < 900:
                        res[k] = t
                return res
        except Exception:
            return {}
    return {}


def ghi_trang_thai_online(data_dict):
    import json

    try:
        serializable = {k: v.isoformat() for k, v in data_dict.items()}
        with open(ONLINE_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(serializable, f)
    except Exception:
        pass


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

# --- MÀN HÌNH ĐĂNG NHẬP NỘI BỘ ---
if not st.session_state.logged_in:
    st.title("🔐 Đăng Nhập Hệ Thống - HongNhungTN")
    st.markdown(
        "### Chào Mừng Bạn Gia Nhập Đội Ngũ Công Ty TNHH Nội Thất Hồng"
        " Nhung Tây Nguyên"
    )
    st.markdown(
        "Vui lòng chọn đúng tên của bạn và nhập mật khẩu nội bộ để truy cập"
        " ứng dụng."
    )

    with st.form("login_form"):
        selected_account = st.selectbox(
            "Chọn tên nhân sự / đội thi công của bạn",
            DANH_SACH_NHAN_SU_CHINH_THUC,
        )
        mat_khau_chung = st.text_input(
            "Mật khẩu nội bộ công ty:", type="password"
        )
        submit_login = st.form_submit_button("Đăng Nhập Hệ Thống")

        if submit_login:
            if mat_khau_chung == "hongnhung2020":
                st.session_state.logged_in = True
                st.session_state.current_user = selected_account

                current_dict = doc_trang_thai_online()
                current_dict[selected_account] = datetime.datetime.now()
                ghi_trang_thai_online(current_dict)

                st.success("Đăng nhập thành công!")
                st.rerun()
            else:
                st.error(
                    "Mật khẩu nội bộ không chính xác! Vui lòng kiểm tra lại mật"
                    " khẩu công ty."
                )

    st.stop()

current_username = st.session_state.current_user
if current_username:
    current_dict = doc_trang_thai_online()
    current_dict[current_username] = datetime.datetime.now()
    ghi_trang_thai_online(current_dict)

# --- SAU KHI ĐĂNG NHẬP THÀNH CÔNG ---
st.sidebar.success(f"👤 Xin chào: **{current_username}**")
if st.sidebar.button("Đăng Xuất"):
    current_dict = doc_trang_thai_online()
    if current_username and current_username in current_dict:
        del current_dict[current_username]
        ghi_trang_thai_online(current_dict)
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.rerun()

# --- THANH TRẠNG THÁI THÀNH VIÊN ĐỒNG BỘ THỜI GIAN THỰC ---
st.sidebar.markdown("---")

active_dict = doc_trang_thai_online()
active_users_list = list(active_dict.keys())

with st.sidebar.expander(
    f"🟢 Trạng Thái Thành Viên ({len(active_users_list)}/{len(DANH_SACH_NHAN_SU_CHINH_THUC)}"
    " online)"
):
    st.markdown("---")
    for member in DANH_SACH_NHAN_SU_CHINH_THUC:
        if member in active_users_list:
            st.sidebar.markdown(f"🟢 {member}")
        else:
            st.sidebar.markdown(f"⚫ {member}")

    if st.button("🔄 Làm Mới Danh Sách Trực Tuyến"):
        st.rerun()

st.sidebar.markdown("---")

# Tiêu đề ứng dụng
st.title("🏆 HongNhungTN - Hệ Thống Quản Lý Công Việc & KPI Nội Bộ")
st.markdown(
    "Chào Mừng Bạn Gia Nhập Đội Ngũ Công Ty TNHH Nội Thất Hồng Nhung Tây Nguyên"
)

# Khởi tạo dữ liệu mẫu cho công việc (có 2 hỗ trợ)
if "df_works" not in st.session_state:
    st.session_state.df_works = pd.DataFrame(
        {
            "Mã Việc": ["V01", "V02", "V03", "V04"],
            "Tên Công trình/Sản phẩm/Hạng mục Nội Thất": [
                "Biệt Thự Phố - C.Hạnh",
                "Căn Hộ - A.Tuấn",
                "Xưởng Mộc HNTN",
                "Xưởng Mộc HNTN",
            ],
            "Nội Dung Công Việc": [
                "Lắp đặt hoàn thiện hệ trần tường",
                "Khảo sát đo đạc hiện trạng thực tế",
                "Thiết kế file cắt ván CNC tủ quần áo",
                "Vận hành máy CNC gia công cắt ván",
            ],
            "Nhân Sự Chính": [
                "Đội trần tường 1 (Lập + Huy)",
                "Trương Thất Lập (Nhân viên kỹ thuật)",
                "Hồ Thậm Hải (Thiết kế ra file CNC)",
                "Đào Minh Mẫn (Phụ trách đứng máy CNC)",
            ],
            "Hỗ Trợ 1": [
                "Khúc Gia Bảo (Nhân viên kỹ thuật)",
                "Không có",
                "Đào Minh Mẫn (Phụ trách đứng máy CNC)",
                "Hồ Thậm Hải (Thiết kế ra file CNC)",
            ],
            "Hỗ Trợ 2": ["Không có", "Không có", "Không có", "Không có"],
            "Hạn Hoàn Thành": [
                "10/04/2026",
                "05/04/2026",
                "06/04/2026",
                "08/04/2026",
            ],
            "Trạng Thái": [
                "Đang thực hiện",
                "Hoàn thành",
                "Hoàn thành",
                "Đang thực hiện",
            ],
        }
    )

if "Dự Án" in st.session_state.df_works.columns:
    st.session_state.df_works = st.session_state.df_works.rename(
        columns={"Dự Án": "Tên Công trình/Sản phẩm/Hạng mục Nội Thất"}
    )

# Tương thích ngược với các phiên bản dữ liệu cũ
if "Nhân Sự Chính" not in st.session_state.df_works.columns:
    if "Người Thực Hiện" in st.session_state.df_works.columns:
        st.session_state.df_works[
            "Nhân Sự Chính"
        ] = st.session_state.df_works["Người Thực Hiện"]
    else:
        st.session_state.df_works["Nhân Sự Chính"] = (
            "Trương Văn Thi (Giám Đốc - Mr. Thi)"
        )

if "Hỗ Trợ 1" not in st.session_state.df_works.columns:
    if "Nhân Sự Hỗ Trợ" in st.session_state.df_works.columns:
        st.session_state.df_works["Hỗ Trợ 1"] = st.session_state.df_works[
            "Nhân Sự Hỗ Trợ"
        ]
    else:
        st.session_state.df_works["Hỗ Trợ 1"] = "Không có"

if "Hỗ Trợ 2" not in st.session_state.df_works.columns:
    st.session_state.df_works["Hỗ Trợ 2"] = "Không có"

if "chat_reports" not in st.session_state:
    st.session_state.chat_reports = []
if "internal_messages" not in st.session_state:
    st.session_state.internal_messages = []

# Menu điều hướng
st.sidebar.title("🛠️ Điều Hướng Quản Lý")
menu = st.sidebar.radio(
    "Chọn Chức Năng:",
    [
        "➕ Giao Việc Mới",
        "📅 Bảng Chấm Công Tự Động",
        "📊 Theo Dõi & Xác Nhận Công Việc",
        "💬 Báo Cáo Hiện Trường (Hình Ảnh / Video)",
        "💭 Phòng Chat Trao Đổi Công Việc Riêng",
    ],
)

# --- 1. GIAO VIỆC MỚI ---
if menu == "➕ Giao Việc Mới":
    st.subheader("➕ Giao Việc Mới Cho Nhân Sự / Đội Thi Công")
    with st.form("form_giao_viec_kpi"):
        c_g1, c_g2 = st.columns(2)
        with c_g1:
            ma_v_moi = st.text_input("Mã Việc (VD: V05)")
            ten_cong_trinh_moi = st.text_input(
                "Tên Công trình/Sản phẩm/Hạng mục Nội Thất"
            )

            # CẬP NHẬT CÁC TAP LỰA CHỌN NHÂN SỰ
            nguoi_nhan_chinh = st.selectbox(
                "Nhân sự phụ trách chính / Đội thi công phụ trách",
                DANH_SACH_NHAN_SU_CHINH_THUC,
            )
            nguoi_ho_tro_1 = st.selectbox(
                "Nhân sự (phụ) hỗ trợ 1 / Đội thi công hỗ trợ 1",
                ["Không có"] + DANH_SACH_NHAN_SU_CHINH_THUC,
            )
            nguoi_ho_tro_2 = st.selectbox(
                "Nhân sự (phụ) hỗ trợ 2 / Đội thi công hỗ trợ 2",
                ["Không có"] + DANH_SACH_NHAN_SU_CHINH_THUC,
            )
        with c_g2:
            han_chot_date =
