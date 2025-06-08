import streamlit as st
import requests

# --- THÔNG TIN CẦN THAY ĐỔI ---
N8N_WEBHOOK_URL = "https://n8n.n2nai.io/webhook-test/my-app"  # Sử dụng URL TEST nếu đang ở chế độ "Listen for Test Event"
# --- KẾT THÚC ---

st.title("🧠 HỆ THỐNG NHẬN DIỆN BỆNH CÁ TỰ ĐỘNG")

# Cho phép tải ảnh lên
uploaded_file = st.file_uploader("📸 Tải ảnh cá lên (jpg, jpeg, png):", type=["jpg", "jpeg", "png"])

# Nếu đã có ảnh
if uploaded_file is not None:
    st.image(uploaded_file, caption="Ảnh bạn vừa tải lên", use_column_width=True)
    st.success("✅ Ảnh đã sẵn sàng để gửi đi.")

    if st.button("🚀 Gửi ảnh để nhận diện"):
        st.info("⏳ Đang gửi ảnh đến hệ thống...")

        try:
            # Gửi ảnh dạng multipart/form-data
            files = {
                "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
            }

            response = requests.post(N8N_WEBHOOK_URL, files=files)

            # Kiểm tra phản hồi
            if response.status_code == 200:
                st.success("🎉 Ảnh đã được xử lý thành công!")
                result = response.json()

                # Hiển thị kết quả nếu có
                if "prediction" in result:
                    st.subheader(f"🔍 Kết quả: **{result['prediction']}**")
                    if "confidence" in result:
                        st.write(f"Độ tin cậy: {result['confidence']:.2f}%")
                else:
                    st.warning("Không có trường 'prediction' trong kết quả trả về.")
                    st.write("Kết quả nhận được:", result)

            else:
                st.error(f"❌ Lỗi HTTP {response.status_code}")
                st.write("Nội dung phản hồi:", response.text)

        except Exception as e:
            st.error(f"🚨 Đã xảy ra lỗi: {e}")
