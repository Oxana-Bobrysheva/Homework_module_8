from django.db import models


class Course(models.Model):
    course_name = (
        models.CharField(
            max_length=200,
            verbose_name="Курс",
            help_text="Введите название курса"
        ),
    )
    preview = (
        models.ImageField(
            upload_to="study/previews",
            blank=True,
            null=True,
            verbose_name="Картинка",
            help_text="Загрузите картинку курса",
        ),
    )
    description = (
        models.TextField(
            blank=True,
            null=True,
            verbose_name="Описание курса",
            help_text="Расскажите о своём курсе",
        ),
    )

    USERNAME_FIELD = "course_name"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ("Курс",)
        verbose_name_plural = "Курсы"
