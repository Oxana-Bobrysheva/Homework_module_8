# Обояшка

Django-проект, который представляет собой платформу на онлайн-обучение. 

## Описание

- Разработка LMS-системы, в которой каждый желающий 
может размещать свои полезные материалы или курсы.

Работа будет над SPA веб-приложением и результатом создания проекта 
будет бэкенд-сервер, который возвращает клиенту JSON-структуры.

## Установка и запуск

1. Клонируйте репозиторий:

    ```bash
    git clone <url-репозитория>
    cd <папка-проекта>
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    .venv\Scripts\activate     # Windows
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Запустите сервер разработки:

    ```bash
    python manage.py runserver
    ```

## Структура проекта

- `subscriptions/` — приложение с формой для создания рассылок, подписчиков.
- `users/` — приложение для работы с пользователем

## Настройка

- Убедитесь, что в `settings.py` добавлено `subscriptions` b 'users' в `INSTALLED_APPS`.


## Настройка подключения к базе данных через `.env`

Для удобства и безопасности параметры подключения к базе данных хранятся в файле `.env`. 
В репозитории есть пример файла `.env.example` с шаблоном переменных окружения.

### Шаги:

1. Создайте копию файла `.env.example` и назовите её `.env`:

```bash
cp .env.example .env
```
2. Отредактируйте .env, указав свои данные подключения к PostgreSQL:

```
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```
3. В settings.py используйте библиотеку 
python-dotenv или django-environ для загрузки переменных окружения.
Пример с python-dotenv:
```
import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```
4. Убедитесь, что файл .env добавлен в .gitignore, чтобы не заливать его в публичный репозиторий.


## Контакты
bobrysheva_oxana@mail.ru

Если есть вопросы, пишите в issues или отправляйте 
pull request.

