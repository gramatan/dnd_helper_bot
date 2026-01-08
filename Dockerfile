FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && mv /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /build

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --only main --no-root

FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app
# Устанавливаем PYTHONPATH, чтобы импорты работали корректно
ENV PYTHONPATH=/app

# Копируем зависимости (site-packages) из сборочного образа
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

