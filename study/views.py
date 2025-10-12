from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from study.models import Course, Lesson, Subscription
from study.paginators import StandardResultsSetPagination
from study.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner
from study.tasks import send_course_update_email


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated or getattr(
                self, "swagger_fake_view", False):
            return Course.objects.none()

        if user.groups.filter(name="moderators").exists():
            return Course.objects.all()
        # Остальные видят только свои курсы
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        if self.action in ["create"]:
            # Создавать и удалять может любой авторизованный, но НЕ модератор
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ["update", "partial_update", "retrieve"]:
            # Обновлять и смотреть детали может владелец ИЛИ модератор
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action in ["destroy"]:
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            # Для списка — любой авторизованный
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        # Вызываем родительский метод для сохранения
        super().perform_update(serializer)
        # Отправляем асинхронное уведомление подписчикам об обновлении курса
        send_course_update_email.delay(serializer.instance.id)


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all().order_by("id")
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        send_course_update_email.delay(serializer.instance.course.id)


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

    def get_queryset(self):
        return Lesson.objects.all()


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

    def get_queryset(self):
        return Lesson.objects.all()

    def perform_update(self, serializer):
        # Вызываем родительский метод для сохранения
        super().perform_update(serializer)
        # Отправляем асинхронное уведомление подписчикам о обновлении курса (через урок)
        send_course_update_email.delay(serializer.instance.course.id)


class LessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Lesson.objects.all()


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_sub = request.user  # Получаем текущего пользователя
        course_id = request.data.get("course_id")

        if not course_id:
            return Response(
                {"error": "course_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Получаем объект курса
        course_item = get_object_or_404(Course, id=course_id)
        # Получаем подписку по пользователю и курсу
        subs_item = Subscription.objects.filter(
            user_sub=user_sub, course=course_item)

        if subs_item.exists():
            # Если подписка есть — удаляем её
            subs_item.first().delete()
            message = "подписка удалена"
        else:
            # Если подписки нет — создаём её
            Subscription.objects.create(
                user_sub=user_sub, course=course_item)
            message = "подписка добавлена"

        # Возвращаем ответ
        return Response({"message": message}, status=status.HTTP_200_OK)
