# Обояшка
Django-проект, который представляет собой платформу на онлайн-обучение.

## Описание
- Разработка LMS-системы, в которой каждый желающий
может размещать свои полезные материалы или курсы.
Работа будет над SPA веб-приложением и результатом создания проекта
будет бэкенд-сервер, который возвращает клиенту JSON-структуры.

Проект развернут на Yandex Cloud (IP: 158.160.128.108) с использованием Docker Compose, включающим Gunicorn, Celery, PostgreSQL, Redis и Nginx. Настроен CI/CD через GitHub Actions для автоматического тестирования и деплоя.

## Технологии
Backend: Django 4.x, Django REST Framework
База данных: PostgreSQL
Кеширование/Очереди: Redis, Celery
Сервер: Gunicorn, Nginx
Контейнеризация: Docker, Docker Compose
CI/CD: GitHub Actions
Хостинг: Yandex Cloud (IP: 158.160.128.108)
### Структура проекта
subscriptions/ — приложение с формой для создания рассылок, подписчиков.
users/ — приложение для работы с пользователем
### Настройка
Убедитесь, что в settings.py добавлено subscriptions и 'users' в INSTALLED_APPS.

В приложение добавились следующие возможности:

    Поле вывода количества уроков
    Новая модель "Платежи" с фикстурами
    Поле вывода уроков по курсу
    Настроена фильтрация для эндпоинта вывода списка платежей
    с возможностями:
        менять порядок сортировки по дате оплаты,
        фильтровать по курсу или уроку,
        фильтровать по способу оплаты.

## Настройка подключения к базе данных через .env
Для удобства и безопасности параметры подключения к базе данных хранятся в файле .env.
В репозитории есть пример файла .env.example с шаблоном переменных окружения.

## Шаги:
Создайте копию файла .env.example и назовите её .env:
cp .env.example .env
Отредактируйте .env, указав свои данные подключения к PostgreSQL и другие переменные:
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=158.160.128.108,localhost
DATABASE_URL=postgresql://user:password@db:5432/study_db
REDIS_URL=redis://redis:6379/0
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
SECRET_KEY: Генерируйте уникальный ключ (например, через python -c "import secrets; print(secrets.token_urlsafe(50))").

## Для тестов в CI используется SQLite in-memory (настроено в settings.py).
В settings.py используйте библиотеку
python-dotenv или django-environ для загрузки переменных окружения.
Пример с python-dotenv:
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
Убедитесь, что файл .env добавлен в .gitignore, чтобы не заливать его в публичный репозиторий.
## Установка и запуск
Локальная настройка (без Docker)
Клонируйте репозиторий:

git clone <url-репозитория>
cd <папка-проекта>
Создайте и активируйте виртуальное окружение:

python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
Установите зависимости:

pip install -r requirements.txt
Выполните миграции и запустите сервер:

python manage.py migrate
python manage.py runserver
Запустите тесты:

python manage.py test
## Настройка и запуск с Docker Compose
Клонируйте репозиторий и перейдите в корневую директорию.
Скопируйте файл .env и заполните его реальными значениями (пароли, ключи).
Запустите: docker-compose build && docker-compose up -d
Выполните миграции: docker-compose exec web python manage.py migrate
Создайте суперпользователя: docker-compose exec web python manage.py createsuperuser
Соберите статику: docker-compose exec web python manage.py collectstatic --noinput
Проверка сервисов
Web: http://localhost:8000 (локально) или http://158.160.128.108 (на сервере)
DB: docker-compose exec db psql -U postgres -d homework_db
Redis: docker-compose exec redis redis-cli ping
Celery: Проверьте логи с помощью docker-compose logs celery
Остановка: docker-compose down

## Настройка удаленного сервера (Yandex Cloud)
Сервер развернут на Yandex Cloud (IP: 158.160.128.108) с Ubuntu 22.04. Все компоненты контейнеризованы через Docker Compose.

Предварительные требования на сервере
Установите Docker и Docker Compose:

sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER  # Перелогиньтесь после
Настройте firewall (ufw):

sudo ufw allow 22/tcp  # SSH
sudo ufw allow 80/tcp  # HTTP
sudo ufw allow 443/tcp  # HTTPS (опционально)
sudo ufw enable
Настройте SSH-доступ по ключам (не пароль):

Сгенерируйте ключ локально: ssh-keygen -t rsa -b 4096.
Добавьте публичный ключ в ~/.ssh/authorized_keys на сервере.
Отключите парольный вход в /etc/ssh/sshd_config: PasswordAuthentication no, затем sudo systemctl restart ssh.
Создайте systemd-сервис для автоматического перезапуска (файл /etc/systemd/system/docker-compose-app.service):

[Unit]
Description=Docker Compose App
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/your/app
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down

[Install]
WantedBy=multi-user.target
Активируйте: sudo systemctl enable docker-compose-app && sudo systemctl start docker-compose-app.
Деплой на сервер
Подключитесь к серверу по SSH.
Клонируйте репо (или используйте GitHub Actions для авто-деплоя).
Создайте .env с реальными переменными (из секретов GitHub или вручную).
Запустите: docker-compose up --build -d.
Приложение доступно на http://158.160.128.108.
## CI/CD с GitHub Actions
Файлы workflow
.github/workflows/ci.yml: Запускает тесты на push/PR.
.github/workflows/deploy.yml: Деплоит на сервер после успешных тестов.
### Запуск workflow
Workflow запускается автоматически на push в любую ветку (тесты) или в main (деплой).
Для ручного запуска: В GitHub Actions выберите workflow и нажмите "Run workflow".
Мониторинг: Проверяйте статус в разделе Actions репозитория. Если тесты/деплой падают, проверьте логи (например, переменные окружения или SSH-доступ).
Шаги деплоя
Тесты проходят в ci.yml.
deploy.yml подключается к серверу по SSH.
Код пуллится из GitHub.
Контейнеры перезапускаются: docker-compose down && docker-compose up --build -d.
Приложение обновляется без downtime (если настроено).
## Контакты
bobrysheva_oxana@mail.ru

Если есть вопросы, пишите в issues или отправляйте
pull request.