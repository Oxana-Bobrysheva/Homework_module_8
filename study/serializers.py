from django.core.serializers import serialize
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from study.models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
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
    lessons_count=serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "course_name",
            "preview",
            "description",
            "lessons_count",
            "lessons"
        ]
    def get_lessons_count(self, obj):
        return obj.lessons.count()



