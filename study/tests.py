from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from study.models import Course, Lesson, Subscription

User = get_user_model()


class LessonCRUDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Создаем группы
        self.moderator_group = Group.objects.create(name="moderators")

        # Создаем пользователей
        self.owner_user = User.objects.create_user(
            username="owner",
            password="password",
            email="owner@example.com"
        )
        self.moderator_user = User.objects.create_user(
            username="moderator",
            password="password",
            email="moderator@example.com"
        )
        self.moderator_user.groups.add(self.moderator_group)
        self.other_user = User.objects.create_user(
            username="other",
            password="password",
            email="other@example.com"
        )

        # Создаем курс
        self.course = Course.objects.create(
            course_name="Test Course",
            description="Test Description",
            owner=self.owner_user,
        )

        # Создаем урок
        self.lesson = Lesson.objects.create(
            lesson_name="Test Lesson",
            lesson_description="Test Description",
            course=self.course,
            owner=self.owner_user,
        )

        # URL-ы для тестов
        self.lesson_list_url = reverse("study:lessons_list")  # /study/lessons/
        self.lesson_detail_url = reverse(
            "study:lessons_retrieve",
            kwargs={"pk": self.lesson.id}
        )  # /study/lessons/<id>/
        self.lesson_create_url = reverse(
            "study:lessons_create"
        )  # /study/lessons/create/
        self.lesson_update_url = reverse(
            "study:lessons_update",
            kwargs={"pk": self.lesson.id}
        )  # /study/lessons/<id>/update/
        self.lesson_delete_url = reverse(
            "study:lessons_delete",
            kwargs={"pk": self.lesson.id}
        )  # /study/lessons/<id>/delete/

        self.subscription_url = reverse(
            "study:subscription_manage"
        )  # Правильный URL через reverse
        self.client = APIClient()

    def test_lesson_list_owner(self):
        """Тест списка уроков для владельца"""
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_lesson_list_moderator(self):
        """Тест списка уроков для модератора"""
        self.client.force_authenticate(user=self.moderator_user)
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_lesson_list_other_user(self):
        """Тест списка уроков для другого пользователя (должен быть пустым)"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_lesson_list_unauthenticated(self):
        """Тест неавторизованного доступа к списку уроков"""
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )  # Исправлено с 403 на 401

    def test_lesson_retrieve_owner(self):
        """Тест просмотра урока владельцем"""
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["lesson_name"], "Test Lesson")

    def test_lesson_retrieve_moderator(self):
        """Тест просмотра урока модератором"""
        self.client.force_authenticate(user=self.moderator_user)
        response = self.client.get(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_retrieve_other_user(self):
        """Тест просмотра урока другим пользователем (должен быть 403)"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.lesson_detail_url)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )  # Исправлено с 404 на 403

    def test_lesson_create_owner(self):
        """Тест создания урока владельцем"""
        self.client.force_authenticate(user=self.owner_user)
        data = {
            "lesson_name": "New Lesson",
            "lesson_description": "New Description",
            "course": self.course.id,
            "video_link": "https://youtube.com/dQw4w9WgXcQ",
        }
        response = self.client.post(self.lesson_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_create_moderator(self):
        """Тест создания урока модератором (должен быть 403)"""
        self.client.force_authenticate(user=self.moderator_user)
        data = {
            "lesson_name": "New Lesson",
            "lesson_description": "New Description",
            "course": self.course.id,
            "video_link": "https://youtube.com/dQw4w9WgXcQ",
        }
        response = self.client.post(self.lesson_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update_owner(self):
        """Тест обновления урока владельцем"""
        self.client.force_authenticate(user=self.owner_user)
        data = {
            "lesson_name": "Updated Lesson",
            "lesson_description": "Updated description",
            "video_link": "https://youtube.com/valid_link",
            "course": self.course.id,
        }
        response = self.client.put(self.lesson_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.lesson_name, "Updated Lesson")

    def test_lesson_update_moderator(self):
        """Тест обновления урока модератором"""
        self.client.force_authenticate(user=self.moderator_user)
        data = {
            "lesson_name": "Updated Lesson",
            "lesson_description": "Updated description",
            "video_link": "https://youtube.com/valid_link",
            "course": self.course.id,
        }
        response = self.client.put(self.lesson_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_update_other_user(self):
        """Тест обновления урока другим пользователем (должен быть 403)"""
        self.client.force_authenticate(user=self.other_user)
        data = {"lesson_name": "Updated by Other"}
        response = self.client.put(self.lesson_update_url, data)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )  # Исправлено с 404 на 403

    def test_lesson_delete_owner(self):
        """Тест удаления урока владельцем"""
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_delete_other_user(self):
        """Тест удаления урока другим пользователем (должен быть 403)"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )  # Исправлено с 404 на 403


class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Создаем пользователей
        self.user = User.objects.create_user(
            username="user",
            password="password",
            email="user@example.com"
        )

        # Создаем курс
        self.course = Course.objects.create(
            course_name="Test Course",
            description="Test Description",
            owner=self.user
        )

        # Правильный URL через reverse
        self.subscription_url = reverse("study:subscription_manage")

    def test_subscribe(self):
        """Тест добавления подписки"""
        self.client.force_authenticate(user=self.user)
        data = {"course_id": self.course.id}
        response = self.client.post(self.subscription_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("подписка добавлена", response.data["message"])
        self.assertTrue(
            Subscription.objects.filter(user_sub=self.user,
                                        course=self.course).exists()
        )

    def test_subscribe_unauthenticated(self):
        """Тест подписки неавторизованным пользователем"""
        client = APIClient(enforce_csrf_checks=False)
        data = {"course_id": self.course.id}
        response = client.post(self.subscription_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscribe_without_course_id(self):
        """Тест подписки без course_id"""
        self.client.force_authenticate(user=self.user)
        data = {}
        response = self.client.post(self.subscription_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
