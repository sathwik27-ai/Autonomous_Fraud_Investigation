
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./
COPY data/ /data/

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --retries=10 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

CMD sh -c "alembic upgrade head || true; uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
