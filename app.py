# import streamlit as st
# import requests
# import base64
#
# st.title("🐟 Hệ thống nhận diện bệnh cá ")
#
# uploaded_file = st.file_uploader("Upload an image of your fish", type=["jpg", "jpeg", "png"])
#
# if uploaded_file:
#     # Đọc ảnh và encode base64
#     img_bytes = uploaded_file.read()
#     base64_img = base64.b64encode(img_bytes).decode("utf-8")
#
#     # Gửi ảnh đến n8n webhook
#     response = requests.post(
#         "https://yennan2275.app.n8n.cloud/webhook-test/fish-dec",
#         json={"image_base64": base64_img}
#     )
#
#     if response.status_code == 200:
#         st.success("✅ Gửi ảnh thành công đến n8n webhook!")
#         st.json(response.json())
#     else:
#         st.error("❌ Gửi ảnh thất bại.")
#         st.text(response.text)


import streamlit as st
import requests
import base64

st.title("Nhận diện bệnh cho cá💅")

uploaded_file = st.file_uploader("Tải ảnh cá lên", type=["jpg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Ảnh cá cần nhận diện", use_column_width=True)

    if st.button("Nhận diện bệnh"):
        img_bytes = uploaded_file.read()
        img_base64 = base64.b64encode(img_bytes).decode()

        payload = {
            "filename": uploaded_file.name,
            "image_base64": img_base64
        }
        response = requests.post("https://yennan2275.app.n8n.cloud/webhook-test/fish-dec", json=payload)

        if response.ok:
            st.success("✅ Kết quả: " + response.json()["message"])
        else:
            st.error("❌ Lỗi khi gửi ảnh tới AI agent.")
