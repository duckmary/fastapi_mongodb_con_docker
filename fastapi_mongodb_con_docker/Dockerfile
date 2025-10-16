FROM python:3.11-slim

WORKDIR /app

# Instala dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia SOLO el código de la API (el compose montará la carpeta en dev)
COPY ./api ./api
