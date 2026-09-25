import datetime
import pandas as pd
import streamlit as st

# Cấu hình giao diện
st.set_page_config(
    page_title="Hệ Thống Quản Lý Công Việc & KPI Nội Thất",
    page_icon="🏆",
    layout="wide",
)

# Tiêu đề ứng dụng
st.title("🏆 Hệ Thống Quản Lý Công Việc & Đánh Giá KPI Nội Bộ")
st.markdown(
    "Theo dõi tiến độ, báo cáo hình ảnh/video hiện trường và chấm điểm KPI (thưởng/phạt, nguyên nhân) tự động."
)

# 1. Danh sách nhân sự thực tế của công ty (Bạn có thể thêm bớt tên nhân viên tại đây)
DANH_SACH_NHAN_SU = [
    "Trương Văn Thi (Giám Đốc / Quản Lý)",
    "Đội Lắp Đặt A (Xưởng & Công Trình)",
    "KTS. Hải (Thiết Kế)",
    "Thợ Mộc Hiền (Sản Xuất)",
    "Nhân sự 05 (Tùy chỉnh)",
]

# Khởi tạo dữ liệu mẫu cho công việc (có đầy đủ các cột KPI, điểm thưởng/phạt, nguyên nhân)
if "df_works" not in st.session_state:
    st.session_state.df_works = pd.DataFrame(
        {
            "Mã Việc": ["V01", "V02", "V03"],
            "Dự Án": [
                "Biệt Thự Phố - C.Hạnh",
                "Căn Hộ - A.Tuấn",
                "Xưởng Mộc NTHN",
            ],
            "Nội Dung Công Việc": [
                "Lắp đặt hoàn thiện tủ bếp gỗ óc chó",
                "Khảo sát đo đạc hiện trạng thực tế",
                "Cắt ván CNC tủ quần áo phòng ngủ",
            ],
            "Người Thực Hiện": [
                "Đội Lắp Đặt A (Xưởng & Công Trình)",
                "KTS. Minh (Thiết Kế)",
                "Thợ Mộc Văn (Sản Xuất)",
            ],
            "Hạn Hoàn Thành": ["2026-04-10", "2026-04-05", "2026-04-08"],
            "Trạng Thái": [
                "Đang thực hiện",
                "Hoàn thành",
                "Chờ duyệt nghiệm thu",
            ],
            "Tiêu Chí KPI Chuẩn": [
                "Đúng bản vẽ kỹ thuật, không trầy xước, bàn giao đúng hạn",
                "Đo đạc chính xác 100%, có biên bản bàn giao mặt bằng",
                "Đúng kích thước ván, tiết kiệm phôi liệu",
            ],
            "Điểm / Thưởng Phạt": ["Thưởng +200k (Đúng hạn)", "Đạt chuẩn 100 điểm", "Trừ -100k (Chậm 1 ngày)"],
            "Nguyên Nhân Không Hoàn Thành": [
                "Không có (Đang tiến hành)",
                "Không có",
                "Hỏng dao cắt CNC phải thay thế giữa chừng",
            ],
        }
    )

# Khởi tạo kho lưu trữ tin nhắn / báo cáo hiện trường (chat & media)
if "chat_reports" not in st.session_state:
    st.session_state.chat_reports = [
        {
            "thoi_gian": "2026-04-04 08:30",
            "nguoi_gui": "Đội Lắp Đặt A (Xưởng & Công Trình)",
            "du_an": "Biệt Thự Phố - C.Hạnh",
            "noi_dung": "Đã vận chuyển vật tư đến công trình, bắt đầu lắp khung tủ bếp.",
            "loai": "Báo cáo tiến độ",
        }
    ]

# Menu chức năng chính
menu = st.sidebar.selectbox(
    "🛠️ Chọn Chức Năng Quản Lý",
    [
        "📊 Theo Dõi Tiến Độ & KPI",
        "💬 Báo Cáo Hiện Trường (Chat & Media)",
        "⭐ Đánh Giá & Tổng Hợp Điểm KPI",
        "➕ Giao Việc Mới & Thiết Lập KPI",
    ],
)

if menu == "📊 Theo Dõi Tiến Độ & KPI":
    st.subheader("📊 Bảng Quản Lý Công Việc & Tiêu Chí KPI")

    # Bộ lọc
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        loc_trang_thai = st.selectbox(
            "Lọc theo trạng thái công việc",
            [
                "Tất cả",
                "Đang thực hiện",
                "Hoàn thành",
                "Chờ duyệt nghiệm thu",
            ],
        )
    with col_f2:
        loc_nhan_su = st.selectbox(
            "Lọc theo nhân sự thực hiện", ["Tất cả"] + DANH_SACH_NHAN_SU
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

    # Cập nhật trạng thái và nguyên nhân không hoàn thành (dành cho nhân viên/quản lý)
    st.markdown("### 🔄 Cập Nhật Tiến Độ & Nguyên Nhân (Dành cho Nhân Sự)")
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
                "Nguyên nhân không hoàn thành / Khó khăn phát sinh (nếu trễ hạn hoặc gặp sự cố):"
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
                    f"Đã cập nhật thành công thông tin cho công việc: {ma_viec_chon}"
                )

elif menu == "💬 Báo Cáo Hiện Trường (Chat & Media)":
    st.subheader(
        "💬 Kênh Báo Cáo Công Việc, Gửi Hình Ảnh & Video Công Trình / Xưởng"
    )

    with st.form("form_bao_cao_ngay", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            ten_nv = st.selectbox("Chọn nhân sự báo cáo", DANH_SACH_NHAN_SU)
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

        noi_dung_bc = st.text_area(
            "Nội dung trao đổi / Mô tả chi tiết công việc trong ngày"
        )

        uploaded_media = st.file_uploader(
            "Đính kèm Hình ảnh sản phẩm / Video công trình (Hỗ trợ JPG, PNG, MP4)",
            type=["png", "jpg", "jpeg", "mp4", "mov"],
            accept_multiple_files=True,
        )

        sub_bc = st.form_submit_button("Gửi Báo Cáo Lên Hệ Thống")
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
                st.success("Đã gửi báo cáo thành công về hệ thống công ty!")
            else:
                st.warning("Vui lòng điền nội dung báo cáo chi tiết.")

    st.markdown("---")
    st.markdown("### 📢 Dòng Thời Gian Báo Cáo Trực Tuyến Từ Hiện Trường")

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

elif menu == "⭐ Đánh Giá & Tổng Hợp Điểm KPI":
    st.subheader(
        "⭐ Bảng Tổng Hợp Tiêu Chí KPI, Điểm Thưởng / Phạt & Đánh Giá Hiệu Suất"
    )

    # Phần dành cho Quản lý chấm điểm / thưởng phạt theo tiêu chí KPI
    st.markdown("### 🛠️ Quản Lý Chấm Điểm & Thưởng/Phạt KPI (Dành cho Quản Lý)")
    with st.form("form_cham_diem_kpi"):
        c_k1, c_k2, c_k3 = st.columns(3)
        with c_k1:
            ma_v_kpi = st.selectbox(
                "Chọn Mã Việc đánh giá KPI",
                st.session_state.df_works["Mã Việc"],
            )
        with c_k2:
            danh_gia_thuong_phat = st.selectbox(
                "Mức độ đạt KPI & Thưởng/Phạt",
                [
                    "Đạt chuẩn xuất sắc (Thưởng +300k)",
                    "Đạt chuẩn tốt (Thưởng +100k)",
                    "Hoàn thành đúng hạn (Đạt 100 điểm)",
                    "Trễ hạn / Lỗi nhỏ (Trừ -100k)",
                    "Lỗi nặng / Hỏng vật tư (Trừ -500k hoặc đền bù)",
                ],
            )
        with c_k3:
            tieu_chi_chuan = st.text_input(
                "Cập nhật Tiêu chí KPI chuẩn mới (nếu có)"
            )

        sub_kpi = st.form_submit_button("Lưu Đánh Giá KPI & Thưởng Phạt")
        if sub_kpi:
            idx = st.session_state.df_works[
                st.session_state.df_works["Mã Việc"] == ma_v_kpi
            ].index
            if not idx.empty:
                st.session_state.df_works.loc[
                    idx, "Điểm / Thưởng Phạt"
                ] = danh_gia_thuong_phat
                if tieu_chi_chuan:
                    st.session_state.df_works.loc[
                        idx, "Tiêu Chí KPI Chuẩn"
                    ] = tieu_chi_chuan
                st.success(
                    f"Đã cập nhật điểm KPI và thưởng phạt thành công cho việc: {ma_v_kpi}"
                )

    st.markdown("---")
    st.markdown("### 📈 Tổng Hợp Điểm Số & Hiệu Suất Theo Công Việc")
    st.dataframe(
        st.session_state.df_works[
            [
                "Mã Việc",
                "Dự Án",
                "Người Thực Hiện",
                "Trạng Thái",
                "Tiêu Chí KPI Chuẩn",
                "Điểm / Thưởng Phạt",
                "Nguyên Nhân Không Hoàn Thành",
            ]
        ],
        use_container_width=True,
    )

elif menu == "➕ Giao Việc Mới & Thiết Lập KPI":
    st.subheader("➕ Giao Việc Mới Kèm Bộ Tiêu Chí KPI Chuẩn")

    with st.form("form_giao_viec_kpi"):
        c_g1, c_g2 = st.columns(2)
        with c_g1:
            ma_v_moi = st.text_input("Mã Việc (VD: V04)")
            du_an_moi = st.text_input("Tên Dự Án Nội Thất")
            nguoi_nhan = st.selectbox(
                "Chọn người thực hiện / đội thi công", DANH_SACH_NHAN_SU
            )
            noi_dung_cv = st.text_area("Mô tả chi tiết công việc cần làm")
        with c_g2:
            han_chot = st.date_input("Hạn hoàn thành (Deadline)")
            tieu_chi_moi = st.text_area(
                "Tiêu chí KPI chuẩn cho việc này (VD: Đúng kích thước, không trầy xước, đúng giờ...)"
            )
            muc_thuong_phat = st.text_input(
                "Quy định Thưởng/Phạt (VD: Vượt tiến độ +200k, Trễ hạn -100k)"
            )

        submit_giao = st.form_submit_button("Xác Nhận Giao Việc & Thiết Lập KPI")
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
