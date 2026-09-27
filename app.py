import datetime
import pandas as pd
import streamlit as st

# Cấu hình giao diện
st.set_page_config(
    page_title="HongNhungTN - Quản Lý Công Việc & KPI",
    page_icon="🏆",
    layout="wide",
)

# Tiêu đề ứng dụng
st.title("🏆 HongNhungTN - Hệ Thống Quản Lý Công Việc & KPI Nội Bộ")
st.markdown(
    "Theo dõi tiến độ, báo cáo hiện trường, quản lý tiêu chí KPI và chấm điểm thưởng/phạt tự động."
)

# Danh sách nhân sự chi tiết theo cơ cấu tổ chức công ty
DANH_SACH_NHAN_SU = [
    "Trương Văn Thi (Giám Đốc - Mr. Thi)",
    (
        "Đặng Thị Hồng Nhung (P.Giám Đốc kiêm Trưởng Phòng Kinh Doanh -"
        " Mrs. Nhung)"
    ),
    "Hồ Ngọc Tú (Kế Toán)",
    "Lê Hoàn (Lái xe điều phối)",
    "Hồ Thậm Hải (Thiết kế ra file CNC)",
    "Đào Minh Mẫn (Phụ trách đứng máy CNC)",
    "Trương Thất Lập",
    "Nông Trọng Huấn",
    "Lê Thanh Hiền",
    "Lê Gia Huy",
    "Khúc Gia Bảo",
    # Các đội thi công chuyên trách & tăng cường
    "Đội trần tường 1 (Lập + Huy)",
    "Đội trần tường 2 (Huấn + Bảo)",
    "Đội lắp đặt 1 (Hiền + Bảo)",
    "Đội lắp đặt 2 (Hải + Mẫn)",
    "Đội lắp đặt 3 tăng cường (Huấn + Huy + Lập)",
]

# Khởi tạo dữ liệu mẫu cho công việc
if "df_works" not in st.session_state:
    st.session_state.df_works = pd.DataFrame(
        {
            "Mã Việc": ["V01", "V02", "V03", "V04"],
            "Dự Án": [
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
                "Trương Thất Lập",
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

# Khởi tạo kho lưu trữ tin nhắn / báo cáo hiện trường (chat & media)
if "chat_reports" not in st.session_state:
    st.session_state.chat_reports = [
        {
            "thoi_gian": "2026-04-04 08:30",
            "nguoi_gui": "Đội trần tường 1 (Lập + Huy)",
            "du_an": "Biệt Thự Phố - C.Hạnh",
            "noi_dung": (
                "Đã bắt đầu triển khai khung xương trần tường tại công trình."
            ),
            "loai": "Báo cáo tiến độ",
        }
    ]

# Menu chức năng chính
st.sidebar.title("🛠️ Điều Hướng Quản Lý")
menu = st.sidebar.radio(
    "Chọn Chức Năng:",
    [
        "📊 Theo Dõi Tiến Độ Công Việc",
        "💬 Báo Cáo Hiện Trường (Chat & Media)",
        "📋 Quản Lý Tiêu Chí KPI Chuẩn",
        "⭐ Chấm Điểm & Thưởng/Phạt KPI",
        "➕ Giao Việc Mới & Thiết Lập KPI",
    ],
)

if menu == "📊 Theo Dõi Tiến Độ Công Việc":
    st.subheader("📊 Bảng Theo Dõi Tiến Độ & Nguyên Nhân Không Hoàn Thành")

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
            "Lọc theo nhân sự / đội thi công", ["Tất cả"] + DANH_SACH_NHAN_SU
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

    st.markdown("### 🔄 Cập Nhật Trạng Thái & Nguyên Nhân Không Hoàn Thành")
    with st.form("form_update_nhan_vien"):
        c_up1, c_up2 = st.columns(2)
        with c_up1:
            ma_viec_chon = st.selectbox(
                "Chọn Mã Việc cần cập nhật", st.session_state.df_works["Mã Việc"]
            )
            trang_thai_moi = st.selectbox(
                "Trạng thái mới",
                [
                    "Đang thực hiện",
                    "Hoàn thành",
                    "Chờ duyệt nghiệm thu",
                    "Tạm hoãn",
                ],
            )
        with c_up2:
            nguyen_nhan_moi = st.text_area(
                "Nhập nguyên nhân không hoàn thành / Khó khăn phát sinh (nếu có):"
            )

        sub_update_nv = st.form_submit_button("Cập Nhật Báo Cáo")
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
                    f"Đã cập nhật thành công cho công việc: {ma_viec_chon}"
                )

elif menu == "💬 Báo Cáo Hiện Trường (Chat & Media)":
    st.subheader(
        "💬 Kênh Báo Cáo Công Việc, Gửi Hình Ảnh & Video Công Trình / Xưởng"
    )

    with st.form("form_bao_cao_ngay", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            ten_nv = st.selectbox(
                "Chọn nhân sự / đội thi công báo cáo", DANH_SACH_NHAN_SU
            )
            ten_du_an = st.text_input(
                "Tên Dự Án hoặc Hạng Mục (VD: Tủ bếp nhà anh Nam)"
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

        noi_dung_bc = st.text_area("Nội dung báo cáo chi tiết")
        uploaded_media = st.file_uploader(
            "Đính kèm Hình ảnh / Video hiện trường",
            type=["png", "jpg", "jpeg", "mp4", "mov"],
            accept_multiple_files=True,
        )

        sub_bc = st.form_submit_button("Gửi Báo Cáo")
        if sub_bc:
            if noi_dung_bc:
                thoi_gian_hien_tai = (
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                )
                st.session_state.chat_reports.insert(
                    0,
                    {
                        "thoi_gian": thoi_gian_hien_tai,
                        "nguoi_gui": ten_nv,
                        "du_an": ten_du_an,
                        "noi_dung": noi_dung_bc,
                        "loai": loai_bc,
                        "media": uploaded_media,
                    },
                )
                st.success("Đã gửi báo cáo thành công!")
            else:
                st.warning("Vui lòng điền nội dung báo cáo.")

    st.markdown("---")
    st.markdown("### 📢 Dòng Thời Gian Báo Cáo Trực Tuyến")
    for report in st.session_state.chat_reports:
        with st.container():
            st.info(
                f"👤 **{report['nguoi_gui']}** | 📁 **Dự án:** {report.get('du_an', 'Chung')} | ⏰ *{report['thoi_gian']}* | 🏷️ *[{report['loai']}]*"
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

elif menu == "📋 Quản Lý Tiêu Chí KPI Chuẩn":
    st.subheader("📋 Danh Mục & Thiết Lập Tiêu Chí KPI Chuẩn Của Công Ty")
    st.markdown(
        "Quản lý và cập nhật các yêu cầu tiêu chuẩn chất lượng kỹ thuật cho từng công việc/hạng mục."
    )

    st.dataframe(
        st.session_state.df_works[
            [
                "Mã Việc",
                "Dự Án",
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

elif menu == "⭐ Chấm Điểm & Thưởng/Phạt KPI":
    st.subheader(
        "⭐ Quản Lý Chấm Điểm KPI, Mức Thưởng & Phạt Cho Từng Nhân Sự"
    )

    st.dataframe(
        st.session_state.df_works[
            [
                "Mã Việc",
                "Dự Án",
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

elif menu == "➕ Giao Việc Mới & Thiết Lập KPI":
    st.subheader("➕ Giao Việc Mới Kèm Bộ Tiêu Chí KPI Chuẩn")

    with st.form("form_giao_viec_kpi"):
        c_g1, c_g2 = st.columns(2)
        with c_g1:
            ma_v_moi = st.text_input("Mã Việc (VD: V05)")
            du_an_moi = st.text_input("Tên Dự Án Nội Thất")
            nguoi_nhan = st.selectbox(
                "Chọn nhân sự / đội thi công phụ trách", DANH_SACH_NHAN_SU
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
            if ma_v_moi and du_an_moi:
                new_row = pd.DataFrame(
                    {
                        "Mã Việc": [ma_v_moi],
                        "Dự Án": [du_an_moi],
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
                    "Vui lòng điền đầy đủ Mã việc và Tên dự án nội thất."
                )
