from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import DateField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email должен быть установлен")
        email = self.normalize_email(email)
        extra_fields.pop('username', None)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите номер телефона",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите место проживания",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_TYPE_CHOICE = [
        ("cash", "наличными"),
        ("to_account", "переводом на счёт"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь",
        related_name="payments",
    )

    payment_date = DateField(
        verbose_name="Дата платежа",
        null=True,
        blank=True,
        help_text="Укажите дату оплаты",
    )

    paid_course = models.ForeignKey(
        "study.Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
        help_text="Укажите оплаченный курс",
    )

    paid_lesson = models.ForeignKey(
        "study.Lesson",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
        help_text="Укажите оплаченный урок",
    )

    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Сумма платежа",
        help_text="Укажите сумму платежа",
    )
    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPE_CHOICE,
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
        null=True,
        blank=True,
    )

    def __str__(self):
        course_or_lesson = self.paid_course if self.paid_course else (self.paid_lesson)
        return (
            f"Пользователь {self.user} оплатил "
            f"{self.payment_amount} {self.get_payment_type_display()} "
            f"за {course_or_lesson}. "
        )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
