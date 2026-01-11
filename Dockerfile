FROM python:3.11-slim

WORKDIR /app

# Sistem paketleri (gcc PyJWT için gerekli)
RUN apt-get update && apt-get install -y \
  gcc \
  default-libmysqlclient-dev \
  pkg-config \
  && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodu
COPY sunucu/ ./sunucu/
COPY tablolari_olustur.py .

# Port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Start command - tablolar önce oluşturulsun
CMD python tablolari_olustur.py && uvicorn sunucu.ana:uygulama --host 0.0.0.0 --port 8000
