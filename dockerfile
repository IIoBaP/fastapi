# Этап сборки
FROM python:3.13.0 AS builder

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Этап результирующего образа
FROM python:3.13.0-slim

WORKDIR /app
COPY --from=builder /app .

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]