FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Création des dossiers data
RUN mkdir -p data/logs data/geoip data/rules && \
    cp .env.example .env

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py", "--help"]