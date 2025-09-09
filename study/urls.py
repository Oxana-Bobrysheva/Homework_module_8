from django.urls import path
from rest_framework.routers import DefaultRouter

from study.apps import StudyConfig
from study.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    SubscriptionAPIView,
)

app_name = StudyConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet,
                basename="course")

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(),
         name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(),
         name="lessons_retrieve"),
    path("lessons/create/", LessonCreateAPIView.as_view(),
         name="lessons_create"),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyAPIView.as_view(),
        name="lessons_delete",
    ),
    path(
        "lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(),
        name="lessons_update"
    ),
    path("subscriptions/", SubscriptionAPIView.as_view(),
         name="subscription_manage"),
]

urlpatterns += router.urls
