from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from onlinelearning.models import Course, Subscription


@shared_task
def send_course_update_notification(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course, is_active=True)

    for subscription in subscribers:
        send_mail(
            subject=f"Обновление курса: {course.title}",
            message=f"Курс {course.title} был обновлен!",
            from_email="ekaterina.kuz@gmail.com",
            recipient_list=[subscription.user.email],
            fail_silently=False,
        )


@shared_task
def send_lesson_update_notification(lesson_id):
    from onlinelearning.models import Lesson, Subscription
    lesson = Lesson.objects.get(id=lesson_id)
    course = lesson.course

    # Проверка, что курс не обновлялся более 4 часов
    if course.updated_at < timezone.now() - timedelta(hours=4):
        subscribers = Subscription.objects.filter(course=course, is_active=True)

        for subscription in subscribers:
            send_mail(
                subject=f"Обновление урока в курсе: {course.title}",
                message=f"Урок '{lesson.title}' в курсе {course.title} был обновлен!",
                from_email="ekaterina.kuz@gmail.com",
                recipient_list=[subscription.user.email],
                fail_silently=False,
            )