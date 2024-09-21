FROM python:3.11-slim AS compile-image
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc curl

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-root

FROM python:3.11-slim AS build-image

COPY --from=compile-image /opt/venv /app/venv

ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

COPY dnd_helper/database/ ./database/
COPY dnd_helper/handlers/ ./handlers/
COPY dnd_helper/keyboards/ ./keyboards/
COPY dnd_helper/utils/ ./utils/
COPY dnd_helper/bot.py .
COPY dnd_helper/main.py .
COPY dnd_helper/config.py .

CMD ["python", "main.py"]
