import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
from inference_sdk import InferenceHTTPClient
from time import sleep
import json
import os

# ------------------------
# Giữ nguyên cấu hình Streamlit & CSS gốc
st.set_page_config(page_title=" Hệ thống phát hiện bệnh ở cá", page_icon="🐟", layout="centered")

# ------------------------
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0A3981;
    }

    [data-testid="stVerticalBlock"] {
        background-color: #EEEEEE !important;
        padding: 2rem !important;
        border-radius: 40px !important; #bo tròn gốc
    }

    /* Chỉnh màu HỆ THỐNG */
    h1 {
        color: #337CCF !important;
        text-align: center !important;
        font-weight: 800 !important;
    }

    .stButton > button {
        background-color: #121481 !important;
        color: white !important;
        border-radius: 12px !important;
        height: 3em !important;
        width: 100% !important;
        font-size: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------
# Giữ nguyên phần mở đầu
st.markdown('<h1 text-align: center;"> Hệ thống phát hiện bệnh ở cá</h1>',unsafe_allow_html=True)

st.markdown("""
🐟 Chúng tôi hiểu rằng mỗi con cá không chỉ là một phần trong đàn – mà còn là cả tâm huyết, công sức và tương lai của người nuôi.  
Vì thế, chúng tôi mang đến một giải pháp hiện đại, dễ sử dụng và hiệu quả: hãy tải lên hình ảnh cá của bạn, hệ thống AI của chúng tôi sẽ tự động phân tích từng chi tiết, nhận diện sớm các dấu hiệu bất thường và phát hiện chính xác những nguy cơ tiềm ẩn về bệnh lý.

📌 Không cần đến các thiết bị đắt tiền hay quy trình rườm rà, giờ đây bạn có thể chủ động giám sát sức khỏe đàn cá của mình mọi lúc, mọi nơi – giảm thiểu thiệt hại, tiết kiệm chi phí và bảo vệ mô hình nuôi trồng một cách bền vững.

🎯 Dù bạn là hộ nuôi cá quy mô nhỏ hay đơn vị sản xuất thủy sản chuyên nghiệp, chúng tôi ở đây để đồng hành – giúp bạn phát hiện bệnh sớm, xử lý nhanh và nuôi cá thông minh hơn mỗi ngày.

👉 Chỉ cần một bức ảnh – phần còn lại, để chúng tôi hỗ trợ bạn.
""")
# ------------------------
# Khởi tạo file lịch sử nếu chưa có
HISTORY_FILE = "history.json"
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

# ------------------------
# Giao diện upload (giữ nguyên)
uploaded_file = st.file_uploader("📷 Vui lòng chọn ảnh cá", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Preview", use_column_width=True)

    image = Image.open(uploaded_file)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    if st.button("📤 Phân tích tình trạng bệnh"):
        webhook_url = "https://yennan.app.n8n.cloud/webhook/fish-detec-app"

        CLIENT = InferenceHTTPClient(
            api_url="https://serverless.roboflow.com",
            api_key="SEDMOs9Km3JrHERSTQXQ"
        )
        result = CLIENT.infer(img_base64, model_id="fish-disease-t6b03/1")

        response = requests.post(webhook_url, json={
            "filename": uploaded_file.name,
            "image_base64": img_base64,
            "result": result
        })

        if response.status_code == 200:
            st.success("✅ Ảnh đã được gửi đến n8n! Vui lòng chờ...")
            sleep(10)
            data = response.json()

            # Lưu kết quả phân tích vào session_state để giữ vĩnh viễn cho đến khi phân tích lại
            st.session_state["ai_reply"] = data["ai_reply"]

            # Lưu lịch sử
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
            history.append({
                "filename": uploaded_file.name,
                "ai_reply": data["ai_reply"]
            })
            with open(HISTORY_FILE, "w") as f:
                json.dump(history, f, indent=2)

        else:
            st.error(f"❌ Gửi thất bại. Mã lỗi: {response.status_code}")

    # ✅ LUÔN HIỂN THỊ KẾT QUẢ PHÂN TÍCH NẾU ĐÃ CÓ
    if "ai_reply" in st.session_state:
        st.subheader("🧾 Kết quả phân tích bệnh:")
        st.text(st.session_state["ai_reply"])

    # Bổ sung: Sidebar Menu LỊCH SỬ
    with st.sidebar:
        st.header("🗂️ Lịch sử tra cứu")
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
            # Hiển thị nút hỏi gửi mail
            st.write("📧 Bạn có muốn nhận kết quả phân tích qua email không?")
            col1, col2 = st.columns(2)

            if col1.button("✉️ Gửi mail", key="send_mail_btn"):
                st.session_state["show_email_input"] = True

            if col2.button("🙅 Không, cảm ơn", key="no_mail_btn"):
                st.session_state["show_email_input"] = False
                st.info("🙏 Cảm ơn bạn đã sử dụng hệ thống!")

        if history:
            for i, item in enumerate(reversed(history[-10:]), 1):
                st.markdown(f"""
                **{i}.** 📁 **Tên file:** {item["filename"]}

                ```
                {item["ai_reply"]}
                ```
                """)
        else:
            st.info("📭 Chưa có lịch sử tra cứu.")

    # Ở ngoài: nếu đã bấm Gửi mail thì hiện form nhập mail
    if st.session_state.get("show_email_input", False):
        user_email = st.text_input("📨 Nhập email của bạn để nhận kết quả:")

        if st.button("🚀 Xác nhận gửi email", key="confirm_send_mail_btn"):
            ai_reply = st.session_state.get("ai_reply", "Không có dữ liệu")
            file_name = uploaded_file.name if uploaded_file else "Unknown"

            # ✅ DỰNG MẪU HỒ SƠ BỆNH ÁN
            medical_record = f"""
🐟 HỒ SƠ BỆNH ÁN CÁ \n

👤 Người nuôi (Email): {user_email}\n

📁 Tên file ảnh:{file_name}\n

🩺 Kết quả chẩn đoán: 
{ai_reply}\n

📋 Hướng dẫn điều trị: 
- Thực hiện đúng các bước chăm sóc, vệ sinh hồ nuôi.
- Áp dụng các phương pháp điều trị như khuyến nghị.
- Liên hệ bác sĩ thủy sản khi cần hỗ trợ thêm.

🙏 Trân trọng,  
Hệ thống phát hiện bệnh ở cá
            """

            payload = {
                "email": user_email,
                "filename": file_name,
                "medical_record": medical_record
            }

            webhook_url = "https://yennan.app.n8n.cloud/webhook/123"

            res = requests.post(webhook_url, json=payload)

            if res.status_code == 200:
                st.success(f"✅ Hồ sơ bệnh án đã được gửi đến {user_email}!")
            else:
                st.error(f"❌ Lỗi: {res.text}")
