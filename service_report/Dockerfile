FROM python:3.12-slim

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY service_report/pyproject.toml service_report/poetry.lock ./
RUN poetry install --only main --no-root

COPY service_report/service_report ./service_report
COPY service_report/report_generator ./service_report/report_generator

ENV PYTHONPATH=/app

CMD ["poetry", "run", "python", "service_report/main.py"]
