from django.contrib import admin

from study.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "course_name", "owner"]  # укажите нужные поля
    search_fields = ["course_name", "description"]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["id", "lesson_name", "course"]
    search_fields = ["lesson_name", "lesson_description"]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user_sub", "course", "created_at")
    search_fields = ("user_sub__email", "course__course_name")
