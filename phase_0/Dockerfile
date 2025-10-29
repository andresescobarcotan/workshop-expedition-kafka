# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app.py /app
RUN pip install fastapi uvicorn aiokafka httpx
ENV PORT=8000
CMD ["bash", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]
