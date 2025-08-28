from django.core.serializers import serialize
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from study.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lessons_count=serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = (
            "course_name",
            "preview",
            "description",
            "lessons_count",
        )
    def get_lessons_count(self, obj):
        return obj.lessons.count()


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            "lesson_name",
            "lesson_description",
            "preview_l",
            "video_link",
            "course",
        )
