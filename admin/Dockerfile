# ---------- Stage 1: Build dependencies ----------
FROM python:3.12-alpine AS builder

ENV POETRY_VERSION=1.8.2

# Установка зависимостей сборки
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev curl

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Создание директории проекта
WORKDIR /app

# Кэшируем pyproject.toml/poetry.lock на раннем этапе
COPY pyproject.toml poetry.lock* ./
# COPY admin/config ./config/

# Установка зависимостей в отдельную директорию
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main

# Копируем остальной код проекта
COPY . .

# ---------- Stage 2: Final runtime image ----------
FROM python:3.12-alpine

# Установка только нужных зависимостей
RUN apk add --no-cache libffi openssl curl ca-certificates && \
    # Установка MinIO Client (mc)
    curl -fsSL https://dl.min.io/client/mc/release/linux-amd64/mc -o /usr/local/bin/mc && \
    chmod +x /usr/local/bin/mc && \
    addgroup -S admin && \
    adduser -D -G admin admin

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /app /app

# Генерация .certs/ с ключами
RUN mkdir -p .certs && \
    openssl genrsa -out .certs/private.key 2048 && \
    openssl rsa -in .certs/private.key -pubout -out .certs/public.key

RUN chown -R admin:admin /app

ENV PYTHONUNBUFFERED=1

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER admin
ENTRYPOINT ["/entrypoint.sh"]
