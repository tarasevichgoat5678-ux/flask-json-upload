# Flask JSON Upload Project

Проект для загрузки и валидации JSON файлов с сохранением в PostgreSQL.

## Требования

- Python 3.8+
- PostgreSQL 12+
- nginx
- gunicorn

## Установка и развертывание

### 1. Установка Python зависимостей

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


### 2. Создание PostgreSQL базы

```sql
CREATE DATABASE flask_db;
CREATE USER username WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE flask_db TO username;
GRANT ALL ON SCHEMA public TO username;
```

### 3. Настройка .env

```bash
DATABASE_URI=postgresql://username:password@localhost:5432/flask_db
```

### 4. Запуск приложения (тестовый)

```bash
python app.py
```

### 5. Запуск с gunicorn + nginx

#### Конфиг gunicorn (gunicorn.conf.py):

```python
workers = 4
bind = "127.0.0.1:8000"
workers_class = "sync"
```

Запуск:

```bash
gunicorn -c gunicorn.conf.py "app:app"
```

#### Конфиг nginx (/etc/nginx/sites-available/flask_app):

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Активация:

```bash
sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Структура проекта

- `app.py` — Точка входа для запуска приложения
- `config.py` — Настройки приложения и базы данных
- `extensions.py` —  Инициализация расширений Flask (SQLAlchemy)
- `models.py` — Модели базы данных SQLAlchemy
- `schemas.py` — Схемы валидации Pydantic
- `routes.py` — Маршруты (Blueprint) для обработки запросов
- `requirements.txt` — зависимости Python
- `.env` — переменные окружения (конфиденциально)
- `README.md` — инструкция по развертыванию
- `first.json` — пример JSON-файла для загрузки
- `templates/` — HTML-шаблоны (Jinja2)
  - `base.html` — базовый шаблон с навигацией
  - `index.html` — главная страница
  - `upload.html` — форма загрузки JSON
  - `entries.html` — таблица всех записей из базы
  - `about.html` — страница «О проекте»

## Формат JSON

```json
[
    {
        "name": "string (< 50 chars)",
        "date": "YYYY-MM-DD_HH:mm"
    }
]
```

## Автор

`Тарасевич Владислав`