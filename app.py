import datetime
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
        "Vui lòng chọn tên của bạn và nhập mật khẩu nội bộ để truy cập ứng"
        " dụng."
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
            # Mật khẩu nội bộ chung cho toàn công ty
            if mat_khau_chung == "hongnhung2020":
                st.session_state.logged_in = True
                st.session_state.current_user = selected_account
                st.success("Đăng nhập thành công!")
                st.rerun()
            else:
                st.error(
                    "Mật khẩu nội bộ không chính xác! Vui lòng kiểm tra lại mật"
                    " khẩu công ty."
                )

    st.stop()

# --- SAU KHI ĐĂNG NHẬP THÀNH CÔNG ---
st.sidebar.success(f"👤 Xin chào: **{st.session_state.current_user}**")
if st.sidebar.button("Đăng Xuất"):
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.rerun()

# Tiêu đề ứng dụng
st.title("🏆 HongNhungTN - Hệ Thống Quản Lý Công Việc & KPI Nội Bộ")
st.markdown(
    "Chào Mừng Bạn Gia Nhập Đội Ngũ Công Ty TNHH Nội Thất Hồng Nhung Tây Nguyên"
)

# Khởi tạo dữ liệu mẫu cho công việc và chuẩn hóa tên cột
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
            "Người Thực Hiện": [
                "Đội trần tường 1 (Lập + Huy)",
                "Trương Thất Lập (Nhân viên kỹ thuật)",
                "Hồ Thậm Hải (Thiết kế ra file CNC)",
                "Đào Minh Mẫn (Phụ trách đứng máy CNC)",
            ],
            "Hạn Hoàn Thành": [
                "2026-04-10",
                "2026-04-05",
                "2026-04-06",
                "2026-04-08",
            ],
            "Trạng Thái": [
                "Đang thực hiện",
                "Hoàn thành",
                "Hoàn thành",
                "Đang thực hiện",
            ],
            "Tiêu Chí KPI Chuẩn": [
                "Đúng bản vẽ kỹ thuật, không trầy xước, bàn giao đúng hạn",
                "Đo đạc chính xác 100%, có biên bản bàn giao mặt bằng",
                "File CNC chính xác kích thước, tối ưu hóa phôi ván",
                "Gia công đúng bản vẽ, không mẻ cạnh, an toàn lao động",
            ],
            "Điểm / Thưởng Phạt": [
                "Thưởng +200k (Đúng hạn)",
                "Đạt chuẩn 100 điểm",
                "Đạt chuẩn 100 điểm",
                "Đang đánh giá",
            ],
            "Nguyên Nhân Không Hoàn Thành": [
                "Không có (Đang tiến hành)",
                "Không có",
                "Không có",
                "Không có",
            ],
        }
    )

# Tự động đồng bộ đổi tên cột cũ thành cột mới nếu session đang lưu bản cũ
if "Dự Án" in st.session_state.df_works.columns:
    st.session_state.df_works = st.session_state.df_works.rename(
        columns={"Dự Án": "Tên Công trình/Sản phẩm/Hạng mục Nội Thất"}
    )

# Khởi tạo kho lưu trữ báo cáo hiện trường và chat nhóm
if "chat_reports" not in st.session_state:
    st.session_state.chat_reports = []
if "internal_messages" not in st.session_state:
    st.session_state.internal_messages = []

# Menu điều hướng chung cho tất cả nhân sự
st.sidebar.title("🛠️ Điều Hướng Quản Lý")
menu = st.sidebar.radio(
    "Chọn Chức Năng:",
    [
        "📊 Theo Dõi & Xác Nhận Công Việc",
        "💬 Báo Cáo Hiện Trường (Hình Ảnh / Video)",
        "💭 Phòng Chat Trao Đổi Công Việc Riêng",
        "📋 Quản Lý & Xem Tiêu Chí KPI",
        "⭐ Chấm Điểm & Thưởng/Phạt KPI",
        "➕ Giao Việc Mới & Thiết Lập KPI",
    ],
)

# --- 1. THEO DÕI & XÁC NHẬN CÔNG VIỆC ---
if menu == "📊 Theo Dõi & Xác Nhận Công Việc":
    st.subheader("📊 Bảng Theo Dõi Tiến Độ & Xác Nhận Công Việc Toàn Công Ty")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        loc_trang_thai = st.selectbox(
            "Lọc theo trạng thái",
            [
                "Tất cả",
                "Đang thực hiện",
                "Hoàn thành",
                "Chờ duyệt nghiệm thu",
                "Tạm hoãn",
            ],
        )
    with col_f2:
        loc_nhan_su = st.selectbox(
            "Lọc theo nhân sự / đội thi công",
            ["Tất cả"] + DANH_SACH_NHAN_SU_CHINH_THUC,
        )

    df_hien_thi = st.session_state.df_works
    if loc_trang_thai != "Tất cả":
        df_hien_thi = df_hien_thi[
            df_hien_thi["Trạng Thái"] == loc_trang_thai
        ]
    if loc_nhan_su != "Tất cả":
        df_hien_thi = df_hien_thi[
            df_hien_thi["Người Thực Hiện"] == loc_nhan_su
        ]

    st.dataframe(df_hien_thi, use_container_width=True)

    st.markdown("### 🔄 Xác Nhận, Cập Nhật Trạng Thái & Nguyên Nhân Công Việc")
    with st.form("form_update_cong_viec"):
        c_up1, c_up2 = st.columns(2)
        with c_up1:
            ma_viec_chon = st.selectbox(
                "Chọn Mã Việc cần cập nhật", st.session_state.df_works["Mã Việc"]
            )
            trang_thai_moi = st.selectbox(
                "Cập nhật Trạng Thái mới",
                [
                    "Đang thực hiện",
                    "Hoàn thành",
                    "Chờ duyệt nghiệm thu",
                    "Tạm hoãn",
                ],
            )
        with c_up2:
            nguyen_nhan_moi = st.text_area(
                "Điền nguyên nhân không hoàn thành / Khó khăn phát sinh (nếu có):"
            )

        sub_update_nv = st.form_submit_button("Xác Nhận & Cập Nhật Công Việc")
        if sub_update_nv:
            idx = st.session_state.df_works[
                st.session_state.df_works["Mã Việc"] == ma_viec_chon
            ].index
            if not idx.empty:
                st.session_state.df_works.loc[idx, "Trạng Thái"] = (
                    trang_thai_moi
                )
                if nguyen_nhan_moi:
                    st.session_state.df_works.loc[
                        idx, "Nguyên Nhân Không Hoàn Thành"
                    ] = nguyen_nhan_moi
                st.success(
                    f"Đã cập nhật thành công trạng thái cho mã việc:"
                    f" {ma_viec_chon}"
                )

# --- 2. BÁO CÁO HIỆN TRƯỜNG ---
elif menu == "💬 Báo Cáo Hiện Trường (Hình Ảnh / Video)":
    st.subheader(
        "💬 Kênh Báo Cáo Công Việc Hàng Ngày, Gửi Hình Ảnh & Video Công Trình"
    )

    with st.form("form_bao_cao_ngay", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            ten_nv = st.text_input(
                "Nhân sự / Đội báo cáo",
                value=st.session_state.current_user,
                disabled=True,
            )
            ten_du_an = st.text_input(
                "Tên Công trình/Sản phẩm/Hạng mục Nội Thất (VD: Tủ bếp nhà anh"
                " Nam)"
            )
        with c2:
            loai_bc = st.selectbox(
                "Loại báo cáo",
                [
                    "Báo cáo tiến độ xưởng mộc",
                    "Báo cáo lắp đặt công trình",
                    "Sự cố / Phát sinh cần xử lý",
                ],
            )

        noi_dung_bc = st.text_area("Nội dung báo cáo chi tiết trong ngày")
        uploaded_media = st.file_uploader(
            "Đính kèm Hình ảnh / Video thực tế",
            type=["png", "jpg", "jpeg", "mp4", "mov"],
            accept_multiple_files=True,
        )

        sub_bc = st.form_submit_button("Gửi Báo Cáo Hiện Trường")
        if sub_bc:
            if noi_dung_bc:
                thoi_gian_hien_tai = (
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                )
                st.session_state.chat_reports.insert(
                    0,
                    {
                        "thoi_gian": thoi_gian_hien_tai,
                        "nguoi_gui": st.session_state.current_user,
                        "du_an": ten_du_an,
                        "noi_dung": noi_dung_bc,
                        "loai": loai_bc,
                        "media": uploaded_media,
                    },
                )
                st.success("Đã gửi báo cáo hiện trường thành công!")
            else:
                st.warning("Vui lòng điền nội dung báo cáo.")

    st.markdown("---")
    st.markdown("### 📢 Dòng Thời Gian Báo Cáo Trực Tuyến")
    for report in st.session_state.chat_reports:
        with st.container():
            st.info(
                f"👤 **{report['nguoi_gui']}** | 📁 **Công trình/Hạng mục:**"
                f" {report.get('du_an', 'Chung')} | ⏰ *{report['thoi_gian']}*"
                f" | 🏷️ *[{report['loai']}]*"
            )
            st.write(f"💬 **Nội dung:** {report['noi_dung']}")
            if "media" in report and report["media"]:
                cols_img = st.columns(len(report["media"]))
                for i, file in enumerate(report["media"]):
                    with cols_img[i]:
                        if file.type.startswith("image"):
                            st.image(
                                file,
                                caption=f"Ảnh: {file.name}",
                                use_container_width=True,
                            )
                        elif file.type.startswith("video"):
                            st.video(file)
            st.markdown("---")

# --- 3. PHÒNG CHAT TRAO ĐỔI CÔNG VIỆC RIÊNG ---
elif menu == "💭 Phòng Chat Trao Đổi Công Việc Riêng":
    st.subheader("💭 Kênh Nhắn Tin & Trao Đổi Công Việc Nội Bộ (Group Chat)")

    with st.form("form_chat_noi_bo", clear_on_submit=True):
        noi_dung_chat = st.text_input("Nhập nội dung trao đổi công việc...")
        sub_chat = st.form_submit_button("Gửi Tin Nhắn")
        if sub_chat:
            if noi_dung_chat:
                thoi_gian_chat = datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                )
                st.session_state.internal_messages.append(
                    {
                        "thoi_gian": thoi_gian_chat,
                        "nguoi_gui": st.session_state.current_user,
                        "noi_dung": noi_dung_chat,
                    }
                )
                st.rerun()
            else:
                st.warning("Vui lòng nhập nội dung tin nhắn.")

    st.markdown("---")
    st.markdown("### 💬 Lịch Sử Trao Đổi Tin Nhắn")
    for msg in reversed(st.session_state.internal_messages):
        st.markdown(
            f"**👤 {msg['nguoi_gui']}**  *({msg['thoi_gian']})*:\n> {msg['noi_dung']}"
        )
        st.markdown("---")

# --- 4. QUẢN LÝ TIÊU CHÍ KPI ---
elif menu == "📋 Quản Lý & Xem Tiêu Chí KPI":
    st.subheader("📋 Danh Mục & Thiết Lập Tiêu Chí KPI Chuẩn Của Công Ty")
    st.dataframe(
        st.session_state.df_works[
            [
                "Mã Việc",
                "Tên Công trình/Sản phẩm/Hạng mục Nội Thất",
                "Người Thực Hiện",
                "Tiêu Chí KPI Chuẩn",
                "Trạng Thái",
            ]
        ],
        use_container_width=True,
    )

    st.markdown("### ✍️ Chỉnh Sửa Tiêu Chí KPI Cho Công Việc")
    with st.form("form_sua_tieu_chi_kpi"):
        c_tc1, c_tc2 = st.columns(2)
        with c_tc1:
            ma_v_tc = st.selectbox(
                "Chọn Mã Việc cần đổi tiêu chí",
                st.session_state.df_works["Mã Việc"],
            )
        with c_tc2:
            tieu_chi_moi_nhap = st.text_area(
                "Nhập nội dung Tiêu chí KPI chuẩn mới:"
            )

        sub_tc = st.form_submit_button("Cập Nhật Tiêu Chí KPI")
        if sub_tc:
            idx = st.session_state.df_works[
                st.session_state.df_works["Mã Việc"] == ma_v_tc
            ].index
            if not idx.empty and tieu_chi_moi_nhap:
                st.session_state.df_works.loc[
                    idx, "Tiêu Chí KPI Chuẩn"
                ] = tieu_chi_moi_nhap
                st.success(
                    f"Đã cập nhật tiêu chí KPI thành công cho mã việc: {ma_v_tc}"
                )

# --- 5. CHẤM ĐIỂM & THƯỞNG PHẠT KPI ---
elif menu == "⭐ Chấm Điểm & Thưởng/Phạt KPI":
    st.subheader(
        "⭐ Quản Lý Chấm Điểm KPI, Mức Thưởng & Phạt Cho Từng Nhân Sự"
    )
    st.dataframe(
        st.session_state.df_works[
            [
                "Mã Việc",
                "Tên Công trình/Sản phẩm/Hạng mục Nội Thất",
                "Người Thực Hiện",
                "Tiêu Chí KPI Chuẩn",
                "Điểm / Thưởng Phạt",
                "Nguyên Nhân Không Hoàn Thành",
            ]
        ],
        use_container_width=True,
    )

    st.markdown("### ⚖️ Thực Hiện Chấm Điểm & Đánh Giá Thưởng/Phạt")
    with st.form("form_cham_diem_kpi"):
        c_k1, c_k2 = st.columns(2)
        with c_k1:
            ma_v_kpi = st.selectbox(
                "Chọn Mã Việc để chấm điểm KPI",
                st.session_state.df_works["Mã Việc"],
            )
        with c_k2:
            danh_gia_thuong_phat = st.selectbox(
                "Chọn Mức Đạt & Thưởng/Phạt tương ứng",
                [
                    "Đạt chuẩn xuất sắc (Thưởng +300k)",
                    "Đạt chuẩn tốt (Thưởng +100k)",
                    "Hoàn thành đúng hạn (Đạt 100 điểm)",
                    "Trễ hạn / Lỗi nhỏ (Trừ -100k)",
                    "Lỗi nặng / Hỏng vật tư (Trừ -500k hoặc đền bù)",
                ],
            )

        sub_kpi = st.form_submit_button("Lưu Điểm & Thưởng/Phạt KPI")
        if sub_kpi:
            idx = st.session_state.df_works[
                st.session_state.df_works["Mã Việc"] == ma_v_kpi
            ].index
            if not idx.empty:
                st.session_state.df_works.loc[
                    idx, "Điểm / Thưởng Phạt"
                ] = danh_gia_thuong_phat
                st.success(
                    f"Đã lưu kết quả chấm điểm KPI cho mã việc: {ma_v_kpi}"
                )

# --- 6. GIAO VIỆC MỚI & THIẾT LẬP KPI ---
elif menu == "➕ Giao Việc Mới & Thiết Lập KPI":
    st.subheader("➕ Giao Việc Mới Kèm Bộ Tiêu Chí KPI Chuẩn")
    with st.form("form_giao_viec_kpi"):
        c_g1, c_g2 = st.columns(2)
        with c_g1:
            ma_v_moi = st.text_input("Mã Việc (VD: V05)")
            ten_cong_trinh_moi = st.text_input(
                "Tên Công trình/Sản phẩm/Hạng mục Nội Thất"
            )
            nguoi_nhan = st.selectbox(
                "Chọn nhân sự / đội thi công phụ trách",
                DANH_SACH_NHAN_SU_CHINH_THUC,
            )
            noi_dung_cv = st.text_area("Mô tả chi tiết công việc cần làm")
        with c_g2:
            han_chot = st.date_input("Hạn hoàn thành (Deadline)")
            tieu_chi_moi = st.text_area(
                "Tiêu chí KPI chuẩn (VD: Đúng kích thước bản vẽ, không trầy xước...)"
            )
            muc_thuong_phat = st.text_input(
                "Quy định Thưởng/Phạt dự kiến (VD: Vượt tiến độ +200k, Trễ hạn -100k)"
            )

        submit_giao = st.form_submit_button("Xác Nhận Giao Việc & Tạo KPI")
        if submit_giao:
            if ma_v_moi and ten_cong_trinh_moi:
                new_row = pd.DataFrame(
                    {
                        "Mã Việc": [ma_v_moi],
                        "Tên Công trình/Sản phẩm/Hạng mục Nội Thất": [
                            ten_cong_trinh_moi
                        ],
                        "Nội Dung Công Việc": [noi_dung_cv],
                        "Người Thực Hiện": [nguoi_nhan],
                        "Hạn Hoàn Thành": [str(han_chot)],
                        "Trạng Thái": ["Đang thực hiện"],
                        "Tiêu Chí KPI Chuẩn": [
                            tieu_chi_moi
                            if tieu_chi_moi
                            else "Hoàn thành đúng yêu cầu kỹ thuật"
                        ],
                        "Điểm / Thưởng Phạt": [
                            muc_thuong_phat
                            if muc_thuong_phat
                            else "Đang đánh giá"
                        ],
                        "Nguyên Nhân Không Hoàn Thành": ["Chưa có"],
                    }
                )
                st.session_state.df_works = pd.concat(
                    [st.session_state.df_works, new_row], ignore_index=True
                )
                st.success(
                    f"Đã giao việc và thiết lập KPI thành công cho **{nguoi_nhan}**!"
                )
            else:
                st.warning(
                    "Vui lòng điền đầy đủ Mã việc và Tên công trình/hạng mục"
                    " nội thất."
                )
