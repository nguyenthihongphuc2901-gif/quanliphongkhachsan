import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime, date

# =========================================================
# CẤU HÌNH ỨNG DỤNG
# =========================================================

st.set_page_config(
    page_title="Hotel Room Management",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "hotel_data.json"

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }

    .block-container {
        padding-top: 1.5rem;
    }

    .hotel-title {
        font-size: 32px;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 5px;
    }

    .hotel-subtitle {
        color: #6b7280;
        margin-bottom: 25px;
    }

    .metric-card {
        background: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .room-card {
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        background: white;
        border: 1px solid #e5e7eb;
        min-height: 180px;
    }

    .room-number {
        font-size: 22px;
        font-weight: 700;
    }

    .status {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin: 5px 0;
    }

    .available {
        background: #dcfce7;
        color: #166534;
    }

    .occupied {
        background: #fee2e2;
        color: #991b1b;
    }

    .cleaning {
        background: #fef3c7;
        color: #92400e;
    }

    .maintenance {
        background: #e0e7ff;
        color: #3730a3;
    }

    .reserved {
        background: #dbeafe;
        color: #1e40af;
    }

    .dirty {
        background: #f3e8ff;
        color: #6b21a8;
    }

    .st-info {
        color: #4b5563;
        font-size: 14px;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# DỮ LIỆU MẶC ĐỊNH
# =========================================================

DEFAULT_ROOMS = [
    {"room": "101", "floor": 1, "type": "Deluxe", "view": "Garden View",
     "price": 1500000, "status": "Trống", "guest": "", "phone": "",
     "checkin": "", "checkout": "", "note": ""},

    {"room": "102", "floor": 1, "type": "Deluxe", "view": "Garden View",
     "price": 1500000, "status": "Trống", "guest": "", "phone": "",
     "checkin": "", "checkout": "", "note": ""},

    {"room": "103", "floor": 1, "type": "Deluxe", "view": "Pool View",
     "price": 1800000, "status": "Trống", "guest": "", "phone": "",
     "checkin": "", "checkout": "", "note": ""},

    {"room": "104", "floor": 1, "type": "Suite", "view": "Sea View",
     "price": 2500000, "status": "Đang ở", "guest": "Nguyễn Văn An",
     "phone": "0901234567", "checkin": "2026-09-27",
     "checkout": "2026-09-30", "note": ""},

    {"room": "201", "floor": 2, "type": "Deluxe", "view": "Sea View",
     "price": 2000000, "status": "Đã đặt", "guest": "Trần Thị Mai",
     "phone": "0912345678", "checkin": "2026-10-01",
     "checkout": "2026-10-04", "note": ""},

    {"room": "202", "floor": 2, "type": "Deluxe", "view": "Sea View",
     "price": 2000000, "status": "Trống", "guest": "", "phone": "",
     "checkin": "", "checkout": "", "note": ""},

    {"room": "203", "floor": 2, "type": "Suite", "view": "Sea View",
     "price": 3000000, "status": "Đang vệ sinh", "guest": "",
     "phone": "", "checkin": "", "checkout": "", "note": ""},

    {"room": "204", "floor": 2, "type": "Suite", "view": "Pool View",
     "price": 2800000, "status": "Trống", "guest": "", "phone": "",
     "checkin": "", "checkout": "", "note": ""},

    {"room": "301", "floor": 3, "type": "Deluxe", "view": "Sea View",
     "price": 2200000, "status": "Bảo trì", "guest": "", "phone": "",
     "checkin": "", "checkout": "", "note": "Điều hòa đang bảo trì"},

    {"room": "302", "floor": 3, "type": "Deluxe", "view": "Sea View",
     "price": 2200000, "status": "Trống", "guest": "", "phone": "",
     "checkin": "", "checkout": "", "note": ""},

    {"room": "303", "floor": 3, "type": "Suite", "view": "Sea View",
     "price": 3200000, "status": "Đang ở", "guest": "Lê Minh Tuấn",
     "phone": "0987654321", "checkin": "2026-09-26",
     "checkout": "2026-09-29", "note": ""},

    {"room": "304", "floor": 3, "type": "Suite", "view": "Sea View",
     "price": 3200000, "status": "Trống", "guest": "", "phone": "",
     "checkin": "", "checkout": "", "note": ""},
]


# =========================================================
# HÀM ĐỌC / LƯU DỮ LIỆU
# =========================================================

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_ROOMS.copy()

    return DEFAULT_ROOMS.copy()


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if "rooms" not in st.session_state:
    st.session_state.rooms = load_data()


# =========================================================
# HÀM TIỆN ÍCH
# =========================================================

def money(value):
    return f"{value:,.0f} VNĐ"


def get_status_class(status):
    mapping = {
        "Trống": "available",
        "Đang ở": "occupied",
        "Đang vệ sinh": "cleaning",
        "Bảo trì": "maintenance",
        "Đã đặt": "reserved",
        "Bẩn": "dirty"
    }

    return mapping.get(status, "available")


def room_dataframe():
    return pd.DataFrame(st.session_state.rooms)


def update_room(room_number, updates):
    for room in st.session_state.rooms:
        if room["room"] == room_number:
            room.update(updates)
            break

    save_data(st.session_state.rooms)


def reset_data():
    st.session_state.rooms = DEFAULT_ROOMS.copy()
    save_data(st.session_state.rooms)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🏨 HOTEL MANAGER")

    st.markdown("---")

    menu = st.radio(
        "MENU",
        [
            "📊 Tổng quan",
            "🛏️ Quản lý phòng",
            "👤 Check-in",
            "🚪 Check-out",
            "📅 Đặt phòng",
            "🧹 Housekeeping",
            "🔧 Bảo trì",
            "📋 Danh sách khách",
            "⚙️ Cài đặt"
        ]
    )

    st.markdown("---")

    st.caption(
        f"Ngày: {datetime.now().strftime('%d/%m/%Y')}"
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="hotel-title">🏨 HOTEL ROOM MANAGEMENT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hotel-subtitle">Hệ thống quản lý phòng khách sạn</div>',
    unsafe_allow_html=True
)


# =========================================================
# TỔNG QUAN
# =========================================================

if menu == "📊 Tổng quan":

    rooms = st.session_state.rooms

    total = len(rooms)

    available = len(
        [r for r in rooms if r["status"] == "Trống"]
    )

    occupied = len(
        [r for r in rooms if r["status"] == "Đang ở"]
    )

    reserved = len(
        [r for r in rooms if r["status"] == "Đã đặt"]
    )

    cleaning = len(
        [r for r in rooms if r["status"] == "Đang vệ sinh"]
    )

    maintenance = len(
        [r for r in rooms if r["status"] == "Bảo trì"]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🏨 Tổng số phòng", total)
    col2.metric("🟢 Phòng trống", available)
    col3.metric("🔴 Đang có khách", occupied)
    col4.metric("🔵 Đã đặt", reserved)

    st.markdown("###")

    col5, col6, col7 = st.columns(3)

    col5.metric("🧹 Đang vệ sinh", cleaning)
    col6.metric("🔧 Bảo trì", maintenance)

    occupancy = (
        occupied / total * 100
        if total > 0 else 0
    )

    col7.metric(
        "📈 Công suất phòng",
        f"{occupancy:.1f}%"
    )

    st.markdown("---")

    st.subheader("Tình trạng phòng")

    status_data = pd.DataFrame({
        "Trạng thái": [
            "Trống",
            "Đang ở",
            "Đã đặt",
            "Đang vệ sinh",
            "Bảo trì"
        ],
        "Số lượng": [
            available,
            occupied,
            reserved,
            cleaning,
            maintenance
        ]
    })

    st.bar_chart(
        status_data.set_index("Trạng thái")
    )

    st.markdown("---")

    st.subheader("Khách đang lưu trú")

    guests = [
        r for r in rooms
        if r["status"] == "Đang ở"
    ]

    if guests:

        guest_df = pd.DataFrame([
            {
                "Phòng": r["room"],
                "Loại phòng": r["type"],
                "Khách": r["guest"],
                "Số điện thoại": r["phone"],
                "Check-in": r["checkin"],
                "Check-out": r["checkout"]
            }
            for r in guests
        ])

        st.dataframe(
            guest_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Hiện chưa có khách đang lưu trú.")


# =========================================================
# QUẢN LÝ PHÒNG
# =========================================================

elif menu == "🛏️ Quản lý phòng":

    st.subheader("🛏️ Quản lý phòng")

    rooms = st.session_state.rooms

    col1, col2, col3 = st.columns(3)

    with col1:
        search = st.text_input(
            "🔎 Tìm phòng",
            placeholder="Nhập số phòng..."
        )

    with col2:
        status_filter = st.selectbox(
            "Trạng thái",
            [
                "Tất cả",
                "Trống",
                "Đang ở",
                "Đã đặt",
                "Đang vệ sinh",
                "Bảo trì",
                "Bẩn"
            ]
        )

    with col3:
        type_filter = st.selectbox(
            "Loại phòng",
            ["Tất cả"] +
            sorted(list(set(r["type"] for r in rooms)))
        )

    filtered = rooms

    if search:
        filtered = [
            r for r in filtered
            if search.lower() in r["room"].lower()
        ]

    if status_filter != "Tất cả":
        filtered = [
            r for r in filtered
            if r["status"] == status_filter
        ]

    if type_filter != "Tất cả":
        filtered = [
            r for r in filtered
            if r["type"] == type_filter
        ]

    st.write(
        f"Hiển thị **{len(filtered)}** / **{len(rooms)}** phòng"
    )

    cols = st.columns(3)

    for index, room in enumerate(filtered):

        with cols[index % 3]:

            css_class = get_status_class(
                room["status"]
            )

            guest_text = (
                room["guest"]
                if room["guest"]
                else "Chưa có khách"
            )

            st.markdown(
                f"""
                <div class="room-card">
                    <div class="room-number">
                        🛏️ Phòng {room["room"]}
                    </div>

                    <span class="status {css_class}">
                        {room["status"]}
                    </span>

                    <div class="st-info">
                        <b>Loại:</b> {room["type"]}<br>
                        <b>View:</b> {room["view"]}<br>
                        <b>Giá:</b> {money(room["price"])} / đêm<br>
                        <b>Khách:</b> {guest_text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "⚙️ Quản lý",
                key=f"manage_{room['room']}",
                use_container_width=True
            ):
                st.session_state.selected_room = room["room"]

    if "selected_room" in st.session_state:

        selected_number = st.session_state.selected_room

        selected = next(
            (
                r for r in rooms
                if r["room"] == selected_number
            ),
            None
        )

        if selected:

            st.markdown("---")

            st.subheader(
                f"⚙️ Quản lý phòng {selected_number}"
            )

            c1, c2 = st.columns(2)

            with c1:

                new_status = st.selectbox(
                    "Trạng thái phòng",
                    [
                        "Trống",
                        "Đang ở",
                        "Đã đặt",
                        "Đang vệ sinh",
                        "Bảo trì",
                        "Bẩn"
                    ],
                    index=[
                        "Trống",
                        "Đang ở",
                        "Đã đặt",
                        "Đang vệ sinh",
                        "Bảo trì",
                        "Bẩn"
                    ].index(selected["status"])
                )

            with c2:

                new_note = st.text_area(
                    "Ghi chú",
                    value=selected.get("note", "")
                )

            if st.button(
                "💾 Lưu thay đổi",
                type="primary"
            ):

                update_room(
                    selected_number,
                    {
                        "status": new_status,
                        "note": new_note
                    }
                )

                st.success(
                    f"Đã cập nhật phòng {selected_number}"
                )

                st.rerun()


# =========================================================
# CHECK-IN
# =========================================================

elif menu == "👤 Check-in":

    st.subheader("👤 Check-in khách")

    available_rooms = [
        r for r in st.session_state.rooms
        if r["status"] == "Trống"
    ]

    if not available_rooms:

        st.warning(
            "Hiện không có phòng trống để check-in."
        )

    else:

        with st.form("checkin_form"):

            col1, col2 = st.columns(2)

            with col1:

                room_number = st.selectbox(
                    "Chọn phòng",
                    [r["room"] for r in available_rooms]
                )

                guest_name = st.text_input(
                    "Họ và tên khách *"
                )

                phone = st.text_input(
                    "Số điện thoại"
                )

            with col2:

                checkin_date = st.date_input(
                    "Ngày check-in",
                    value=date.today()
                )

                checkout_date = st.date_input(
                    "Ngày check-out"
                )

                note = st.text_area(
                    "Ghi chú"
                )

            submit = st.form_submit_button(
                "✅ Xác nhận Check-in",
                type="primary"
            )

            if submit:

                if not guest_name.strip():

                    st.error(
                        "Vui lòng nhập tên khách."
                    )

                elif checkout_date <= checkin_date:

                    st.error(
                        "Ngày check-out phải sau ngày check-in."
                    )

                else:

                    update_room(
                        room_number,
                        {
                            "status": "Đang ở",
                            "guest": guest_name,
                            "phone": phone,
                            "checkin": str(checkin_date),
                            "checkout": str(checkout_date),
                            "note": note
                        }
                    )

                    st.success(
                        f"Check-in thành công cho khách {guest_name} - phòng {room_number}"
                    )

                    st.rerun()


# =========================================================
# CHECK-OUT
# =========================================================

elif menu == "🚪 Check-out":

    st.subheader("🚪 Check-out khách")

    occupied_rooms = [
        r for r in st.session_state.rooms
        if r["status"] == "Đang ở"
    ]

    if not occupied_rooms:

        st.info(
            "Hiện không có khách cần check-out."
        )

    else:

        room_number = st.selectbox(
            "Chọn phòng check-out",
            [r["room"] for r in occupied_rooms]
        )

        room = next(
            r for r in occupied_rooms
            if r["room"] == room_number
        )

        st.info(
            f"""
            **Phòng:** {room["room"]}  
            **Khách:** {room["guest"]}  
            **Check-in:** {room["checkin"]}  
            **Check-out dự kiến:** {room["checkout"]}  
            **Giá phòng:** {money(room["price"])} / đêm
            """
        )

        if st.button(
            "🚪 Xác nhận Check-out",
            type="primary"
        ):

            update_room(
                room_number,
                {
                    "status": "Đang vệ sinh",
                    "guest": "",
                    "phone": "",
                    "checkin": "",
                    "checkout": ""
                }
            )

            st.success(
                f"Phòng {room_number} đã check-out và chuyển sang trạng thái Đang vệ sinh."
            )

            st.rerun()


# =========================================================
# ĐẶT PHÒNG
# =========================================================

elif menu == "📅 Đặt phòng":

    st.subheader("📅 Đặt phòng")

    available_rooms = [
        r for r in st.session_state.rooms
        if r["status"] == "Trống"
    ]

    if not available_rooms:

        st.warning(
            "Không còn phòng trống."
        )

    else:

        with st.form("booking_form"):

            room_number = st.selectbox(
                "Phòng",
                [r["room"] for r in available_rooms]
            )

            col1, col2 = st.columns(2)

            with col1:

                guest_name = st.text_input(
                    "Tên khách"
                )

                phone = st.text_input(
                    "Số điện thoại"
                )

            with col2:

                checkin_date = st.date_input(
                    "Ngày nhận phòng"
                )

                checkout_date = st.date_input(
                    "Ngày trả phòng"
                )

            submit = st.form_submit_button(
                "📅 Xác nhận đặt phòng",
                type="primary"
            )

            if submit:

                if not guest_name.strip():

                    st.error(
                        "Vui lòng nhập tên khách."
                    )

                elif checkout_date <= checkin_date:

                    st.error(
                        "Ngày trả phòng phải sau ngày nhận phòng."
                    )

                else:

                    update_room(
                        room_number,
                        {
                            "status": "Đã đặt",
                            "guest": guest_name,
                            "phone": phone,
                            "checkin": str(checkin_date),
                            "checkout": str(checkout_date)
                        }
                    )

                    st.success(
                        f"Đã đặt phòng {room_number} cho {guest_name}."
                    )

                    st.rerun()


# =========================================================
# HOUSEKEEPING
# =========================================================

elif menu == "🧹 Housekeeping":

    st.subheader("🧹 Quản lý Housekeeping")

    rooms = st.session_state.rooms

    hk_rooms = [
        r for r in rooms
        if r["status"] in [
            "Đang vệ sinh",
            "Bẩn"
        ]
    ]

    if not hk_rooms:

        st.success(
            "Không có phòng cần vệ sinh."
        )

    else:

        for room in hk_rooms:

            col1, col2, col3, col4 = st.columns(
                [1, 2, 2, 1]
            )

            with col1:
                st.write(
                    f"### {room['room']}"
                )

            with col2:
                st.write(
                    f"Loại: {room['type']}"
                )

            with col3:

                status = st.selectbox(
                    "Trạng thái",
                    ["Đang vệ sinh", "Bẩn", "Trống"],
                    index=[
                        "Đang vệ sinh",
                        "Bẩn",
                        "Trống"
                    ].index(room["status"]),
                    key=f"hk_{room['room']}"
                )

            with col4:

                if st.button(
                    "Cập nhật",
                    key=f"hk_save_{room['room']}"
                ):

                    update_room(
                        room["room"],
                        {
                            "status": status
                        }
                    )

                    st.success(
                        f"Đã cập nhật phòng {room['room']}"
                    )

                    st.rerun()


# =========================================================
# BẢO TRÌ
# =========================================================

elif menu == "🔧 Bảo trì":

    st.subheader("🔧 Quản lý bảo trì")

    maintenance_rooms = [
        r for r in st.session_state.rooms
        if r["status"] == "Bảo trì"
    ]

    if maintenance_rooms:

        for room in maintenance_rooms:

            with st.expander(
                f"🔧 Phòng {room['room']} - {room['type']}"
            ):

                st.write(
                    f"**Ghi chú:** {room.get('note', '')}"
                )

                note = st.text_area(
                    "Nội dung bảo trì",
                    value=room.get("note", ""),
                    key=f"maintenance_note_{room['room']}"
                )

                if st.button(
                    "💾 Lưu",
                    key=f"maintenance_save_{room['room']}"
                ):

                    update_room(
                        room["room"],
                        {
                            "note": note
                        }
                    )

                    st.success("Đã lưu.")


    else:

        st.success(
            "Hiện không có phòng đang bảo trì."
        )

    st.markdown("---")

    st.subheader("Đưa phòng vào bảo trì")

    normal_rooms = [
        r for r in st.session_state.rooms
        if r["status"] in ["Trống", "Bẩn"]
    ]

    if normal_rooms:

        room_number = st.selectbox(
            "Chọn phòng",
            [r["room"] for r in normal_rooms]
        )

        note = st.text_area(
            "Lý do bảo trì"
        )

        if st.button(
            "🔧 Chuyển sang bảo trì",
            type="primary"
        ):

            update_room(
                room_number,
                {
                    "status": "Bảo trì",
                    "note": note
                }
            )

            st.success(
                f"Phòng {room_number} đã chuyển sang Bảo trì."
            )

            st.rerun()


# =========================================================
# DANH SÁCH KHÁCH
# =========================================================

elif menu == "📋 Danh sách khách":

    st.subheader("📋 Danh sách khách")

    guests = [
        r for r in st.session_state.rooms
        if r["guest"]
    ]

    if guests:

        guest_df = pd.DataFrame([
            {
                "Phòng": r["room"],
                "Khách hàng": r["guest"],
                "Điện thoại": r["phone"],
                "Trạng thái": r["status"],
                "Check-in": r["checkin"],
                "Check-out": r["checkout"],
                "Loại phòng": r["type"],
                "View": r["view"]
            }
            for r in guests
        ])

        search_guest = st.text_input(
            "🔎 Tìm tên khách"
        )

        if search_guest:

            guest_df = guest_df[
                guest_df["Khách hàng"]
                .str.contains(
                    search_guest,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            guest_df,
            use_container_width=True,
            hide_index=True
        )

        csv = guest_df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "⬇️ Xuất danh sách khách CSV",
            csv,
            "danh_sach_khach.csv",
            "text/csv"
        )

    else:

        st.info(
            "Chưa có thông tin khách."
        )


# =========================================================
# CÀI ĐẶT
# =========================================================

elif menu == "⚙️ Cài đặt":

    st.subheader("⚙️ Cài đặt hệ thống")

    st.markdown(
        """
        ### Thông tin hệ thống

        - Tên hệ thống: Hotel Room Management
        - Nền tảng: Streamlit
        - Dữ liệu: JSON
        - Tiền tệ: VNĐ
        - Quản lý trạng thái phòng
        - Quản lý khách lưu trú
        - Check-in / Check-out
        - Đặt phòng
        - Housekeeping
        - Bảo trì
        """
    )

    st.markdown("---")

    st.subheader("📊 Dữ liệu phòng")

    rooms_df = pd.DataFrame(
        st.session_state.rooms
    )

    st.dataframe(
        rooms_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    st.subheader("⚠️ Khôi phục dữ liệu")

    st.warning(
        "Thao tác này sẽ xóa các thay đổi hiện tại và đưa hệ thống về dữ liệu mẫu ban đầu."
    )

    if st.button(
        "🔄 Khôi phục dữ liệu mẫu"
    ):

        reset_data()

        st.success(
            "Đã khôi phục dữ liệu mẫu."
        )

        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Hotel Room Management System • Streamlit • "
    f"Cập nhật {datetime.now().strftime('%d/%m/%Y %H:%M')}"
)
