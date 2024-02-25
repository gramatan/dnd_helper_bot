FROM python:3.11-slim AS compile-image
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.11-slim AS build-image

COPY --from=compile-image /opt/venv /app/venv

ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

COPY src/database/ ./database/
COPY src/db/ ./db/
COPY src/handlers/ ./handlers/
COPY src/keyboards/ ./keyboards/
COPY src/utils/ ./utils/
COPY src/bot.py .
COPY src/main.py .
COPY src/config.py .

CMD ["python", "main.py"]
