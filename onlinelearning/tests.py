from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from .models import Course, Lesson, Subscription


class LessonCRUDTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="qwerty123"
        )
        self.moderator = User.objects.create_user(
            email="manager@example.com", password="manager123"
        )
        self.moderator.groups.create(name="moderators")

        self.course = Course.objects.create(title="Test Course", owner=self.user)

        self.valid_data = {
            "title": "Test Lesson",
            "course": self.course.id,
            "video_link": "https://www.youtube.com/watch?v=test",
        }

    # Создание
    def test_create_lesson(self):
        url = reverse("onlinelearning:lessons-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_create_lesson_invalid_url(self):
        url = reverse("onlinelearning:lessons-list")
        invalid_data = {**self.valid_data, "video_link": "https://invalid.com/video"}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Список уроков
    def test_get_lessons_list(self):
        Lesson.objects.create(
            title="Test Lesson",
            course=self.course,
            owner=self.user,
            video_link="https://www.youtube.com/watch?v=test",
        )
        url = reverse("onlinelearning:lessons-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_get_single_lesson(self):
        lesson = Lesson.objects.create(
            title="Test Lesson",
            course=self.course,
            owner=self.user,
            video_link="https://www.youtube.com/watch?v=test",
        )
        url = reverse("onlinelearning:lessons-detail", args=[lesson.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Lesson")

    # Обновление урока
    def test_update_lesson(self):
        lesson = Lesson.objects.create(
            title="Test Lesson",
            course=self.course,
            owner=self.user,
            video_link="https://www.youtube.com/watch?v=test",
        )
        url = reverse("onlinelearning:lessons-detail", args=[lesson.id])
        updated_data = {**self.valid_data, "title": "Updated Lesson"}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson.refresh_from_db()
        self.assertEqual(lesson.title, "Updated Lesson")

    # Удаление урока
    def test_delete_lesson(self):
        lesson = Lesson.objects.create(
            title="Test Lesson",
            course=self.course,
            owner=self.user,
            video_link="https://www.youtube.com/watch?v=test",
        )
        url = reverse("onlinelearning:lessons-detail", args=[lesson.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 1)

    # Разрешение на удаление урока модератором
    def test_delete_lesson_by_moderator(self):
        lesson = Lesson.objects.create(
            title="Test Lesson",
            course=self.course,
            owner=self.user,
            video_link="https://www.youtube.com/watch?v=test",
        )
        url = reverse("onlinelearning:lessons-detail", args=[lesson.id])
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# Тесты по подпискам


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="qwerty567"
        )
        self.other_user = User.objects.create_user(
            email="other_users@example.com", password="ytrew235"
        )
        self.course = Course.objects.create(title="Test Course", owner=self.user)

    # -Подписаться/отписаться
    def test_subscribe_unsubscribe(self):
        url = reverse("onlinelearning:subscriptions")
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    # Создание подписки
    def test_is_subscribed_flag(self):
        # Создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        url = reverse("course-detail", args=[self.course.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_subscribed"])

    # Разрешения на подписку
    def test_subscribe_unauthorized(self):
        url = reverse("onlinelearning:subscriptions")
        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscribe_to_nonexistent_course(self):
        url = reverse("onlinelearning:subscriptions")
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {"course_id": 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
