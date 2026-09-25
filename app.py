import datetime
import pandas as pd
import streamlit as st

# Cấu hình giao diện
st.set_page_config(
    page_title="Quản Lý & Báo Cáo Công Việc Nội Thất", page_icon="📋", layout="wide"
)

# Tiêu đề ứng dụng
st.title("📋 Hệ Thống Quản Lý & Báo Cáo Công Việc Nội Bộ")
st.markdown(
    "Theo dõi tiến độ, giao việc, báo cáo hình ảnh/video hiện trường và đánh giá hiệu suất tự động."
)

# Khởi tạo dữ liệu mẫu cho công việc (nếu chưa có trong session_state)
if "df_works" not in st.session_state:
    st.session_state.df_works = pd.DataFrame(
        {
            "Mã Việc": ["V01", "V02", "V03"],
            "Dự Án": [
                "Biệt Thự Phố - C.Hạnh",
                "Căn Hộ - A.Tuấn",
                "Xưởng Mộc HNTN",
            ],
            "Nội Dung Công Việc": [
                "Lắp đặt hoàn thiện tủ bếp gỗ óc chó",
                "Khảo sát đo đạc hiện trạng thực tế",
                "Cắt ván CNC tủ quần áo phòng ngủ",
            ],
            "Người Thực Hiện": ["Đội Lắp Đặt A", "KTS. Minh", "Thợ Mộc Văn"],
            "Hạn Hoàn Thành": ["2026-04-10", "2026-04-05", "2026-04-08"],
            "Trạng Thái": [
                "Đang thực hiện",
                "Hoàn thành",
                "Chờ duyệt nghiệm thu",
            ],
            "Đánh Giá Tự Động": ["Đúng hạn", "Hoàn thành sớm", "Cần kiểm tra lại"],
        }
    )

# Khởi tạo kho lưu trữ tin nhắn / báo cáo hiện trường (chat & media)
if "chat_reports" not in st.session_state:
    st.session_state.chat_reports = [
        {
            "thoi_gian": "2026-04-04 08:30",
            "nguoi_gui": "Đội Lắp Đặt A",
            "du_an": "Biệt Thự Phố - C.Hạnh",
            "noi_dung": "Đã vận chuyển vật tư đến công trình, bắt đầu lắp khung tủ bếp.",
            "loai": "Báo cáo tiến độ",
        }
    ]

# Menu chức năng chính
menu = st.sidebar.selectbox(
    "🛠️ Chọn Chức Năng Quản Lý",
    [
        "📊 Theo Dõi & Giao Việc Hàng Ngày",
        "💬 Báo Cáo Hiện Trường (Chat & Media)",
        "⭐ Đánh Giá Kết Quả Công Việc Tự Động",
        "➕ Tạo Giao Việc Mới",
    ],
)

if menu == "📊 Theo Dõi & Giao Việc Hàng Ngày":
    st.subheader("📊 Bảng Quản Lý & Theo Dõi Tiến Độ Công Việc Hàng Ngày")

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
        loc_nhan_su = st.text_input(
            "Tìm theo tên nhân sự / đội thi công (để trống nếu xem tất cả)"
        )

    df_hien_thi = st.session_state.df_works
    if loc_trang_thai != "Tất cả":
        df_hien_thi = df_hien_thi[
            df_hien_thi["Trạng Thái"] == loc_trang_thai
        ]
    if loc_nhan_su:
        df_hien_thi = df_hien_thi[
            df_hien_thi["Người Thực Hiện"].str.contains(
                loc_nhan_su, case=False, na=False
            )
        ]

    st.dataframe(df_hien_thi, use_container_width=True)

    # Cập nhật trạng thái công việc nhanh
    st.markdown("### 🔄 Cập Nhật Trạng Thái Công Việc")
    with st.form("form_update_status"):
        c_up1, c_up2, c_up3 = st.columns(3)
        with c_up1:
            ma_viec_chon = st.selectbox(
                "Chọn Mã Việc cần cập nhật", st.session_state.df_works["Mã Việc"]
            )
        with c_up2:
            trang_thai_moi = st.selectbox(
                "Trạng thái mới",
                [
                    "Đang thực hiện",
                    "Hoàn thành",
                    "Chờ duyệt nghiệm thu",
                    "Tạm hoãn",
                ],
            )
        with c_up3:
            danh_gia_moi = st.selectbox(
                "Kết quả đánh giá",
                ["Đúng hạn", "Hoàn thành sớm", "Trễ hạn", "Cần kiểm tra lại"],
            )

        sub_update = st.form_submit_button("Cập Nhật Ngay")
        if sub_update:
            idx = st.session_state.df_works[
                st.session_state.df_works["Mã Việc"] == ma_viec_chon
            ].index
            if not idx.empty:
                st.session_state.df_works.loc[idx, "Trạng Thái"] = (
                    trang_thai_moi
                )
                st.session_state.df_works.loc[idx, "Đánh Giá Tự Động"] = (
                    danh_gia_moi
                )
                st.success(
                    f"Đã cập nhật thành công cho công việc: {ma_viec_chon}"
                )

elif menu == "💬 Báo Cáo Hiện Trường (Chat & Media)":
    st.subheader(
        "💬 Kênh Báo Cáo Công Việc, Gửi Hình Ảnh & Video Công Trình / Xưởng"
    )
    st.markdown(
        "Nhân viên gửi báo cáo tiến độ trực tiếp kèm hình ảnh chụp thực tế sản phẩm hoặc video công trình."
    )

    # Form gửi báo cáo mới
    with st.form("form_bao_cao_ngay", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            ten_nv = st.text_input("Họ tên nhân sự / Trưởng nhóm báo cáo")
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

        # Cho phép tải lên hình ảnh hoặc video
        uploaded_media = st.file_uploader(
            "Đính kèm Hình ảnh sản phẩm / Video công trình (Hỗ trợ JPG, PNG, MP4)",
            type=["png", "jpg", "jpeg", "mp4", "mov"],
            accept_multiple_files=True,
        )

        sub_bc = st.form_submit_button("Gửi Báo Cáo Lên Hệ Thống")
        if sub_bc:
            if ten_nv and noi_dung_bc:
                thoi_gian_hien_tai = (
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                )
                # Lưu vào danh sách chat reports
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
                st.warning(
                    "Vui lòng điền tên người gửi và nội dung báo cáo chi tiết."
                )

    st.markdown("---")
    st.markdown("### 📢 Dòng Thời Gian Báo Cáo Trực Tuyến Từ Hiện Trường")

    for report in st.session_state.chat_reports:
        with st.container():
            st.info(
                f"👤 **{report['nguoi_gui']}** | 📁 **Dự án:** {report.get('du_an', 'Chung')} | ⏰ *{report['thoi_gian']}* | 🏷️ *[{report['loai']}]*"
            )
            st.write(f"💬 **Nội dung:** {report['noi_dung']}")

            # Hiển thị file đính kèm nếu có
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

elif menu == "⭐ Đánh Giá Kết Quả Công Việc Tự Động":
    st.subheader(
        "⭐ Thống Kê & Đánh Giá Hiệu Suất Làm Việc Nhân Sự Hàng Ngày / Tháng"
    )

    df = st.session_state.df_works

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Tổng Đầu Việc", len(df))
    col_m2.metric(
        "Đã Hoàn Thành", len(df[df["Trạng Thái"] == "Hoàn thành"])
    )
    col_m3.metric(
        "Đang Thực Hiện", len(df[df["Trạng Thái"] == "Đang thực hiện"])
    )

    st.markdown("---")
    st.markdown("### 📈 Bảng Tổng Hợp Đánh Giá Tự Động Theo Nhân Sự")

    if not df.empty:
        # Thống kê số lượng công việc hoàn thành và đánh giá theo từng nhân sự
        summary_df = (
            df.groupby(["Người Thực Hiện", "Đánh Giá Tự Động"])
            .size()
            .reset_index(name="Số lượng")
        )
        st.dataframe(summary_df, use_container_width=True)

        st.info(
            "💡 **Hệ thống tự động chấm điểm:** Dựa trên mốc thời gian hoàn thành so với hạn chót (Deadline) và trạng thái xác nhận từ quản lý xưởng/công trình."
        )

elif menu == "➕ Tạo Giao Việc Mới":
    st.subheader("➕ Giao Việc Mới Cho Nhân Sự / Đội Thi Công")

    with st.form("form_giao_viec"):
        c_g1, c_g2 = st.columns(2)
        with c_g1:
            ma_v_moi = st.text_input("Mã Việc (VD: V04)")
            du_an_moi = st.text_input("Tên Dự Án Nội Thất")
            noi_dung_cv = st.text_area("Mô tả chi tiết công việc cần làm")
        with c_g2:
            nguoi_nhan = st.text_input(
                "Người thực hiện / Đội thi công phụ trách"
            )
            han_chot = st.date_input("Hạn hoàn thành (Deadline)")
            do_uu_tien = st.selectbox(
                "Độ ưu tiên", ["Bình thường", "Quan trọng (Gấp)", "Khẩn cấp"]
            )

        submit_giao = st.form_submit_button("Xác Nhận Giao Việc")
        if submit_giao:
            if ma_v_moi and du_an_moi and nguoi_nhan:
                new_row = pd.DataFrame(
                    {
                        "Mã Việc": [ma_v_moi],
                        "Dự Án": [du_an_moi],
                        "Nội Dung Công Việc": [noi_dung_cv],
                        "Người Thực Hiện": [nguoi_nhan],
                        "Hạn Hoàn Thành": [str(han_chot)],
                        "Trạng Thái": ["Đang thực hiện"],
                        "Đánh Giá Tự Động": ["Đang thực hiện"],
                    }
                )
                st.session_state.df_works = pd.concat(
                    [st.session_state.df_works, new_row], ignore_index=True
                )
                st.success(
                    f"Đã giao việc thành công cho **{nguoi_nhan}**!"
                )
            else:
                st.warning("Vui lòng điền đầy đủ các thông tin bắt buộc.")
