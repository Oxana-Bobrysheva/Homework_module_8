from django.core.serializers import serialize
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from study.models import Course, Lesson, Subscription
from study.validators import validate_video_link


class LessonSerializer(serializers.ModelSerializer):
    # Поле video-link с валидатором
    materials = serializers.CharField(validators=[validate_video_link])

    class Meta:
        model = Lesson
        fields = [
            "id",
            "lesson_name",
            "lesson_description",
            "preview_l",
            "video_link",
            "course",
        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "course_name",
            "preview",
            "description",
            "lessons_count",
            "lessons",
            "is_subscribed"
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            from study.models import Subscription
            return Subscription.objects.filter(user_sub=user, course=obj).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):

    user_email = serializers.CharField(source='user_sub.email', read_only=True)  # Email пользователя
    course_name = serializers.CharField(source='course.course_name', read_only=True)  # Название курса

    class Meta:
        model = Subscription
        fields = [
            "id",
            "user_sub",  # ID пользователя
            "course",    # ID курса
            "created_at", # Дата подписки
            "user_email",  # Дополнительное поле (read-only)
            "course_name"  # Дополнительное поле (read-only)
        ]
        read_only_fields = ["id", "created_at"]