FROM python:3.12-slim

# Update Debian OS packages
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY backend/api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend

CMD ["celery", "-A", "backend.worker.celery_app.celery_app", "worker", "--loglevel=info"]
