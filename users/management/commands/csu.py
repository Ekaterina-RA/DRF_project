from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from onlinelearning.models import Course, Lesson


class Command(BaseCommand):
    help = "Создание групп пользователей"

    def handle(self, *args, **options):
        # Группа модераторов
        moderators, created = Group.objects.get_or_create(name="moderators")

        # Получаем разрешения
        content_types = ContentType.objects.get_for_models(Course, Lesson)
        permissions = Permission.objects.filter(
            content_type__in=content_types.values(),
            codename__in=[
                "view_course",
                "change_course",
                "view_lesson",
                "change_lesson",
            ],
        )

        # Назначаем разрешения
        moderators.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS("Группы успешно созданы"))
