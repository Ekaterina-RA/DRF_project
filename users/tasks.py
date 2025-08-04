from celery import shared_task
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone

User = get_user_model()


@shared_task
def check_inactive_users():
    """Блокирует пользователей, которые не появлялись более месяца"""
    inactive_threshold = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(
        last_login__lt=inactive_threshold,
        is_active=True
    )

    for user in inactive_users:
        user.is_active = False
        user.save()