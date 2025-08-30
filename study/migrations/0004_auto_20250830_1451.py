from django.db import migrations

def fix_owner_ids(apps, schema_editor):
    Lesson = apps.get_model('study', 'Lesson')
    User = apps.get_model('users', 'User')

    # Получаем первого существующего пользователя — можно заменить на нужный ID
    owner = User.objects.first()
    if owner is None:
        # Если пользователей нет — ничего не делаем
        return

    # Исправляем все уроки с owner_id=2 (не существующий) на существующего пользователя
    lessons_to_fix = Lesson.objects.filter(owner_id=2)
    lessons_to_fix.update(owner=owner)

class Migration(migrations.Migration):

    dependencies = [
        ('study', '0003_course_owner_lesson_owner'),
    ]

    operations = [
        migrations.RunPython(fix_owner_ids),
    ]
