import os
from celery import Celery

# Устанавливаем настройки Django по умолчанию для программы 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаём экземпляр приложения Celery
app = Celery('config')  # Название приложения (может быть 'your_project_name')

# Загружаем настройки из Django settings.py (с префиксом CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи из всех приложений Django
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
