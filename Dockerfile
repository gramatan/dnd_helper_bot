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

COPY dnd_helper dnd_helper

FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем исходный код и зависимости из предыдущего этапа
COPY --from=builder /build/dnd_helper ./dnd_helper
COPY --from=builder /build/pyproject.toml ./pyproject.toml
COPY --from=builder /build/poetry.lock ./poetry.lock

# Копируем зависимости (site-packages) из сборочного образа
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/poetry /usr/local/bin/poetry

# Устанавливаем PYTHONPATH, чтобы импорты работали корректно
ENV PYTHONPATH=/app

# Запускаем приложение
CMD ["python", "dnd_helper/main.py"]
