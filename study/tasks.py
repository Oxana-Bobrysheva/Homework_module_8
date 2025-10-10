import datetime
from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    """
    Асинхронная задача: отправляет письма подписчикам курса об обновлении.
    """
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course)  # Все подписки на курс

        if not subscriptions:
            return f"Нет подписчиков для курса {course.course_name}"

        subject = f"Обновление курса: {course.course_name}"
        message = f"Привет! Курс '{course.course_name}' был обновлён. Проверьте новые материалы на сайте."
        from_email = settings.DEFAULT_FROM_EMAIL

        recipient_list = [sub.user_sub.email for sub in subscriptions]  # Email из user_sub

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )

        return f"Письма отправлены {len(recipient_list)} подписчикам курса {course.course_name}"

    except Course.DoesNotExist:
        return "Курс не найден"
    except Exception as e:
        return f"Ошибка при отправке: {str(e)}"


@shared_task
def block_inactive_users():
    """
    Задача для блокировки пользователей, которые не заходили более 30 дней.
    """
    # Рассчитываем дату 30 дней назад
    thirty_days_ago = timezone.now() - datetime.timedelta(days=30)

    # Фильтруем активных пользователей, у которых last_login старше 30 дней
    inactive_users = User.objects.filter(
        last_login__lt=thirty_days_ago,
        is_active=True
    )

    # Блокируем их (устанавливаем is_active=False)
    count = inactive_users.update(is_active=False)

    print(f"Заблокировано {count} пользователей.")

    return count