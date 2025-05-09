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
├── deploy/docker                 # конфигурация сторонних сервисов
│   ├── postgres.env
│   ├── postgres.example.env
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

* **ruff** — линтинг и автофиксы по PEP8
* **mypy** — проверка типов
* **black** — автоформатирование кода
* **isort** — сортировка импортов
* **pyupgrade** — обновление синтаксиса Python
* **pre-commit-hooks** — базовые проверки (`check-yaml`, `trailing-whitespace` и т.п.)

---

## 5. Docker Compose: запуск и интеграция сервисов

### Запуск всех сервисов:

```bash
docker-compose up -d
```

### Подключение к сервисам:

| Сервис               | Адрес                   | Примечание                               |
| -------------------- | ----------------------- | ---------------------------------------- |
| PostgreSQL           | `localhost:5432`        | user/password из `postgres.env`          |
| pgAdmin              | `http://localhost:5050` | UI для работы с БД                       |
| Kafka                | `localhost:9092`        | Kafka брокер                             |
| Schema Registry      | `http://localhost:8085` | REST-интерфейс схем                      |
| Kafka UI             | `http://localhost:8081` | UI-интерфейс Kafka (Provectus Kafka UI)  |
| MinIO API            | `http://localhost:9000` | S3-совместимое API, creds из `minio.env` |
| MinIO Console UI     | `http://localhost:9001` | Web UI для управления бакетами           |


### Авторизация Kafka UI:

Логин и пароль задаются в `.env`:

```
admin / admin
```

### Авторизация pgAdmin:

По умолчанию доступ через:

```
Email: pgadmin@example.com
Пароль: admin
```

Настраивается в `pgadmin.env`

### Авторизация MinioUI:

Логин и пароль задаются в `.env`:

По умолчанию доступ через
```
minioadmin / minioadmin
```

### Используемые `.env` файлы:

* `postgres.env` — настройки PostgreSQL
* `pgadmin.env` — логин/пароль для pgAdmin
* `kafka-kraft.env` — параметры Kafka без ZooKeeper (KRaft)
* `schema-registry.env` — включение поддержки без ZooKeeper
* `kafka-ui.env` — конфигурация интерфейса Kafka с авторизацией
