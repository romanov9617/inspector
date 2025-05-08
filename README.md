# Inspector Monorepo

Добро пожаловать в монорепозиторий проекта **Inspector**.

В этом репозитории размещены все микросервисы проекта, общая инфраструктура для запуска, конфигурация сторонних сервисов, а также правила работы с git и коммитами.

---

## 1. GitFlow: процесс работы с задачами

Мы придерживаемся упрощённой модели GitFlow:

* **main** — стабильная ветка, всегда отражает текущее состояние production.
* **develop** — основная ветка разработки.
* **feat/** — ветки для новых фич.
* **bugfix/** — ветки для исправления ошибок.
* **hotfix/** — срочные исправления production.

### Как начать работу над задачей:

1. Убедитесь, что ваша локальная ветка `develop` обновлена:

   ```bash
   git checkout develop
   git pull origin develop
   ```
2. Создайте новую ветку от `develop`:

   ```bash
   git checkout -b feature/название-задачи
   ```

   * Название ветки должно быть на **английском языке** и в **kebab-case** (например, `feature/user-login-endpoint`).
3. После завершения — откройте pull request в `develop`.
4. Пройдите код-ревью.
5. После слияния — удалите ветку.

---

## 2. Правила наименования коммитов

Мы используем следующую структуру коммитов:

```
<тип>: <краткое описание>
```

* Все коммиты должны быть на **английском языке**.

**Типы:**

* `feat` — новая функциональность
* `fix` — исправление бага
* `docs` — изменения в документации
* `refactor` — рефакторинг без изменения поведения
* `test` — добавление/обновление тестов
* `chore` — технические коммиты (обновление зависимостей, настройки CI и т.п.)

**Примеры:**

```
feat: add endpoint for task retrieval
fix: fix date parsing error
refactor: simplify token validation logic
```

---

## 3. Структура проекта

```
inspector/
├── README.md               # общий readme по проекту
├── docker-compose.yml      # общий docker-compose для запуска всех сервисов
├── deploy/                 # конфигурация сторонних сервисов
│   ├── postgres/
│   ├── nats/
│   └── ...
├── service-auth/          # сервис аутентификации
│   ├── README.md
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── src/
├── service-inspection/    # сервис инспекций
│   ├── README.md
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── src/
└── service-reports/       # сервис отчётов
    ├── README.md
    ├── Dockerfile
    ├── docker-compose.yml
    └── src/
```

Каждый сервис является изолированным компонентом:

* имеет собственный `README.md`, в котором описана его цель, API, зависимости;
* содержит `Dockerfile` и при необходимости `docker-compose.yml` для локальной разработки.

---

## 4. Pre-commit хуки

В проекте рекомендуется использовать [`pre-commit`](https://pre-commit.com/) для запуска автоматических проверок кода: форматирование, статический анализ, поиск секретов и пр.

Для этого:

1. Установите pre-commit:

   ```bash
   pip install pre-commit
   ```
2. Установите хуки:

   ```bash
   pre-commit install
   ```
3. Убедитесь, что в проекте настроен `.pre-commit-config.yaml` с нужными проверками.

### Используемые хуки:

* **ruff** — линтинг и автофиксы по PEP8, заменяет flake8 и часть функциональности pylint.
* **mypy** — проверка типов по аннотациям.
* **black** — автоформатирование кода.
* **isort** — сортировка импортов.
* **pyupgrade** — автоматическое обновление синтаксиса под современную версию Python.
* **pre-commit-hooks** — базовые проверки вроде `end-of-file-fixer`, `trailing-whitespace`, `check-yaml`.

---

## 5. Docker Compose: запуск и интеграция сервисов

### 🚀 Запуск всех сервисов:

```bash
docker-compose up -d
```

### 🌐 Подключение к сервисам:

| Сервис           | Адрес                   | Примечание                      |
| ---------------- | ----------------------- | ------------------------------- |
| PostgreSQL       | `localhost:5432`        | user/password из `postgres.env` |
| pgAdmin          | `http://localhost:5050` | UI для работы с БД              |
| Kafka            | `localhost:9092`        | Kafka брокер                    |
| Schema Registry  | `http://localhost:8085` | REST-интерфейс схем             |
| Redpanda Console | `http://localhost:8081` | UI-интерфейс Kafka              |

---
