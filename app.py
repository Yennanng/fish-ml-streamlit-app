# app.py
import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="Fish ML", layout="centered", page_icon="🐟")
st.markdown("<h1 style='text-align: center;'>Fish ML</h1>", unsafe_allow_html=True)

optimal_threshold = 0.11576238
st.markdown(f"**Optimal threshold:** `{optimal_threshold}`")

uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["jpg", "jpeg", "png"],
    help="Limit 200MB per file - JPG, PNG, JPEG"
)

if uploaded_file is not None:
    file_details = {
        "filename": uploaded_file.name,
        "size (MB)": round(uploaded_file.size / (1024 * 1024), 2)
    }
    st.write(f"**File details:** `{file_details['filename']}` ({file_details['size (MB)']} MB)")

    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)

    dummy_probability = np.random.uniform(0, 1)
    result = "This fish is not diseased" if dummy_probability > optimal_threshold else "This fish is diseased"
    st.markdown(f"**Prediction:** `{result}`, `({dummy_probability:.8f})`")