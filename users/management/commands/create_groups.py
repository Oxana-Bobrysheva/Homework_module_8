from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from study.models import Course, Lesson


class Command(BaseCommand):
    help = "Create default user groups"

    def handle(self, *args, **options):
        # Создаем группу модераторов
        moderators_group, created = Group.objects.get_or_create(
            name="moderators")

        if created:
            # Получаем разрешения для моделей
            course_content_type = ContentType.objects.get_for_model(Course)
            lesson_content_type = ContentType.objects.get_for_model(Lesson)

            # Добавляем права на просмотр и изменение (но не создание/удаление)
            view_course_permission = Permission.objects.get(
                codename="view_course", content_type=course_content_type
            )
            change_course_permission = Permission.objects.get(
                codename="change_course", content_type=course_content_type
            )
            view_lesson_permission = Permission.objects.get(
                codename="view_lesson", content_type=lesson_content_type
            )
            change_lesson_permission = Permission.objects.get(
                codename="change_lesson", content_type=lesson_content_type
            )

            moderators_group.permissions.add(
                view_course_permission,
                change_course_permission,
                view_lesson_permission,
                change_lesson_permission,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    "Successfully created moderators group with permissions"
                )
            )
        else:
            self.stdout.write("Moderators group already exists")
