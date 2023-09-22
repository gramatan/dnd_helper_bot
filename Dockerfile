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

COPY /database/ ./database/
COPY /db/ ./db/
COPY /handlers/ ./handlers/
COPY /keyboards/ ./keyboards/
COPY /utils/ ./utils/
COPY bot.py .
COPY main.py .
COPY config.py .

CMD ["python", "main.py"]
