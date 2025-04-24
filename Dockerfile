FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.8.3

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && pip install psycopg2-binary

COPY app ./app
COPY migrations ./migrations
COPY alembic.ini .

ENV PYTHONPATH=/app

CMD ["poetry", "run", "uvicorn", "app.asgi:app", "--host", "0.0.0.0", "--port", "8000"] 