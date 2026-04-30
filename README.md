# Контрольная работа №4

Проект выполнен на `FastAPI` и закрывает задания `9.1`, `10.1`, `10.2`, `11.1` и `11.2`:

- миграции БД через `Alembic`;
- ресурс `products` на `SQLAlchemy`;
- REST-эндпоинты `users`, `auth`, `products`;
- пользовательские исключения и единый формат ошибок;
- валидация входных JSON-моделей;
- синхронные и асинхронные тесты.

## Структура проекта

- `app/api/` — роутеры, каждый набор эндпоинтов в отдельном файле;
- `app/models/` — каждая модель в отдельном файле;
- `app/exceptions/` — пользовательские исключения;
- `app/core/` — БД, зависимости, обработчики ошибок, безопасность, in-memory хранилище;
- `alembic/versions/` — миграции;
- `tests/` — синхронные и асинхронные тесты.

## Установка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

При необходимости можно создать `.env` на основе `.env.example`, но по умолчанию используется SQLite-файл `app.db`.

## Применение миграций

```bash
alembic upgrade head
```

Миграции:

- `0001_create_products_table` — создаёт таблицу `products` и добавляет 2 записи;
- `0002_add_product_description` — добавляет обязательное поле `description`.

## Запуск приложения

```bash
uvicorn app.main:app --reload
```

или

```bash
python main.py
```

## Основные эндпоинты и статусы

### Users

- `POST /users` — `201`, `409`, `422`
- `GET /users/{user_id}` — `200`, `404`, `422`
- `DELETE /users/{user_id}` — `204`, `404`, `422`

### Auth

- `POST /auth/login` — `200`, `401`, `422`
- `GET /auth/me` — `200`, `401`
- `DELETE /auth/logout` — `204`, `401`

### Products

- `GET /products` — `200`
- `POST /products` — `201`, `422`
- `GET /products/{product_id}` — `200`, `404`, `422`

## Проверка функциональности

Примеры запросов:

```bash
curl -X POST http://127.0.0.1:8000/users ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"student\",\"age\":22,\"email\":\"student@example.com\",\"password\":\"password1\",\"phone\":\"+79990001122\"}"
```

```bash
curl -X POST http://127.0.0.1:8000/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"student\",\"password\":\"password1\"}"
```

```bash
curl http://127.0.0.1:8000/products/1
```

Важно: логин и пароль передаются только через JSON-тело запроса.

## Тестирование

Синхронные и асинхронные тесты запускаются так:

```bash
pytest
```

В проекте проверяются:

- успешное создание пользователя;
- ошибки валидации и дублирования пользователя;
- авторизация и получение текущего пользователя;
- получение и создание товаров;
- асинхронные сценарии `create/get/delete` для `/users` через `httpx.AsyncClient` и `ASGITransport`;
- изоляция состояния in-memory хранилища между тестами.
