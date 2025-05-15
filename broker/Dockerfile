FROM python:3.12-slim

RUN apt-get update && apt-get install -y gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*

ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY admin/pyproject.toml admin/poetry.lock ./

RUN poetry install --no-root

COPY broker/src ./broker
COPY admin      ./admin

CMD ["python", "broker/broker.py"]
