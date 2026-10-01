FROM python:3.12-slim

# Update Debian OS packages to available patched versions
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY backend/api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend

EXPOSE 8000

CMD ["uvicorn", "backend.api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
