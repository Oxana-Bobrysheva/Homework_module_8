from django.db import models
from django.db.models import SET_NULL


class Course(models.Model):
    course_name = (
        models.CharField(
            max_length=200, verbose_name="Курс", help_text="Введите название курса"
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

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = ("Курс",)
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    lesson_name = (
        models.CharField(
            max_length=250, verbose_name="Урок", help_text="Введите название урока"
        ),
    )
    lesson_description = (
        models.TextField(
            verbose_name="Описание урока", help_text="Расскажите об уроке"
        ),
    )
    preview_l = (
        models.ImageField(
            upload_to="study/preview_l",
            blank=True,
            null=True,
            verbose_name="Картинка",
            help_text="Загрузите картинку урока",
        ),
    )
    video_link = (
        models.TextField(
            blank=True,
            null=True,
            verbose_name="Ссылка на видео",
            help_text="Введите ссылку на видео",
        ),
    )
    course = (
        models.ForeignKey(
            Course,
            on_delete=models.SET_NULL,
            verbose_name="Курс",
            help_text="Укажите курс",
        ),
    )

    class Meta:
        verbose_name = ("Урок",)
        verbose_name_plural = "Уроки"
