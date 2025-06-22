FROM python:3.11-slim

# Cài các thư viện hệ thống để chạy OpenCV và inference_sdk
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .


# Cài thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Tạo config cho Streamlit
RUN mkdir -p ~/.streamlit && \
    echo "[server]\nheadless = true\nenableCORS = false\n" > ~/.streamlit/config.toml

EXPOSE 8080

# Chạy Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
