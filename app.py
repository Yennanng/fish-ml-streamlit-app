import streamlit as st
import requests
import base64
import io

# --- THÔNG TIN CẦN THAY ĐỔI ---
# Dán Webhook Test URL mà bạn đã sao chép từ n8n ở Bước 2 vào đây
N8N_WEBHOOK_URL = "https://n8n.n2nai.io/webhook/3020bb98-bbef-4302-b3d4-0903c1031192" # THAY THẾ XXXXXX BẰNG URL CỦA BẠN

# Nếu bạn có dùng API Key trong Webhook của n8n (phần "Authentication"), thì điền vào đây
# Nếu chưa dùng, cứ để rỗng hoặc xóa dòng này đi để đơn giản cho lần đầu
# N8N_API_KEY = "" # Ví dụ: "your_secret_key_for_n8n_webhook"
# --- KẾT THÚC THÔNG TIN CẦN THAY ĐỔI ---

st.title("CÁ BẠN BỊ GÌ VẬY???🐟")

# Cho phép người dùng tải ảnh lên
uploaded_file = st.file_uploader("Tải ảnh cá lên đây", type=["jpg", "jpeg", "png"])

# Nếu có ảnh được tải lên
if uploaded_file is not None:
    # Hiển thị ảnh đã tải
    st.image(uploaded_file, caption="Ảnh bạn đã tải lên.", use_column_width=True)
    st.write("")
    st.success("Ảnh đã sẵn sàng!")

    # Nút để bắt đầu nhận diện
    if st.button("😼 Nhận diện bệnh"):
        st.info("Đang gửi ảnh đến hệ thống để phân tích...")
        try:
            # Đọc dữ liệu ảnh (bytes) và mã hóa thành chuỗi Base64
            # Base64 là cách để biến ảnh thành một chuỗi văn bản để dễ dàng gửi qua internet
            bytes_data = uploaded_file.getvalue()
            base64_encoded_image = base64.b64encode(bytes_data).decode('utf-8')

            # Chuẩn bị dữ liệu (payload) để gửi đi dưới dạng JSON
            # Chúng ta gửi chuỗi Base64 của ảnh và tên file
            payload = {
                "image_base64": base64_encoded_image,
                "filename": uploaded_file.name,
                # Bạn có thể thêm các thông tin khác ở đây nếu muốn, ví dụ "user_id": "nguoi_dung_123"
            }

            # Chuẩn bị các tiêu đề (headers) cho yêu cầu HTTP
            headers = {
                "Content-Type": "application/json", # Báo cho n8n biết chúng ta gửi dữ liệu JSON
                # Nếu bạn có dùng N8N_API_KEY ở trên, thì thêm dòng này vào:
                # "X-API-Key": N8N_API_KEY
            }

            # Gửi yêu cầu POST đến Webhook của n8n
            # 'json=payload' sẽ tự động chuyển payload thành JSON và đặt Content-Type
            response = requests.post(N8N_WEBHOOK_URL, json=payload, headers=headers)

            # Kiểm tra kết quả phản hồi từ n8n
            if response.status_code == 200:
                st.success("🎉 Ảnh đã được xử lý! Đang nhận kết quả...")
                # n8n sẽ trả về kết quả, chúng ta đọc nó
                n8n_result = response.json()

                # Giả sử n8n sẽ trả về kết quả nhận diện trong trường 'prediction'
                if "prediction" in n8n_result:
                    st.subheader(f"✨ Kết quả dự đoán: **{n8n_result['prediction']}**")
                    if "confidence" in n8n_result:
                        st.write(f"Độ tin cậy: {n8n_result['confidence']:.2f}%")
                else:
                    st.warning("Không nhận được kết quả dự đoán cụ thể từ hệ thống. Vui lòng thử lại sau.")
                    st.write("Chi tiết phản hồi từ n8n:", n8n_result) # Để debug

            else:
                st.error(f"❌ Có lỗi xảy ra khi gửi hoặc xử lý ảnh trên n8n. Mã lỗi: {response.status_code}")
                st.write("Thông báo lỗi từ n8n:", response.text) # Để debug thêm

        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ Lỗi kết nối mạng hoặc không thể gửi yêu cầu đến n8n: {e}")
            st.info("Vui lòng kiểm tra lại URL Webhook hoặc kết nối internet của bạn.")
        except Exception as e:
            st.error(f"🚨 Đã xảy ra lỗi không mong muốn: {e}")