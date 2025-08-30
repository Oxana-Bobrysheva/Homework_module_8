from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создание тестовых пользователей"

    def handle(self, *args, **options):
        users_data = [
            {
                "email": "user3@example.com",
                "phone": "+79991234567",
                "city": "Москва",
                "first_name": "Иван",
                "last_name": "Иванов",
                "password": "testpass123",
            },
            {
                "email": "user2@example.com",
                "phone": "+79997654321",
                "city": "Санкт-Петербург",
                "first_name": "Мария",
                "last_name": "Петрова",
                "password": "testpass123",
            },
            {
                "email": "user4@example.com",
                "phone": "+79997654324",
                "city": "Санкт-Петербург",
                "first_name": "Мари",
                "last_name": "Перова",
                "password": "testpass123",
            },
        ]

        created_count = 0
        for user_data in users_data:
            if not User.objects.filter(email=user_data["email"]).exists():
                user = User.objects.create_user(
                    email=user_data["email"],
                    phone=user_data["phone"],
                    city=user_data["city"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    password=user_data["password"],
                )
                created_count += 1
                self.stdout.write(f"Создан пользователь: {user.email}")

        self.stdout.write(
            self.style.SUCCESS(f"Успешно создано {created_count} пользователей")
        )
