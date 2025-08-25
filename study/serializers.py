from rest_framework.serializers import ModelSerializer

from study.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "course_name",
            "preview",
            "description",
        )


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
