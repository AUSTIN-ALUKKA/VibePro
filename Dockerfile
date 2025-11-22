FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home appuser
WORKDIR /app

FROM base AS builder
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

FROM base
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY backend /app/backend
WORKDIR /app/backend

ENV PATH="/home/appuser/.local/bin:$PATH"
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["gunicorn","-k","uvicorn.workers.UvicornWorker","app.main:app","--bind","0.0.0.0:8000","--workers","1","--log-level","info"]
