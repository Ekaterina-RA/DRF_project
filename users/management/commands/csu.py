from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from onlinelearning.models import Course, Lesson


class Command(BaseCommand):
    help = "Создание группы модераторов"

    def handle(self, *args, **options):
        # Создаем группу модераторов
        moderators_group, created = Group.objects.get_or_create(name="moderators")

        # Получаем контент-типы для моделей
        course_content_type = ContentType.objects.get_for_model(Course)
        lesson_content_type = ContentType.objects.get_for_model(Lesson)

        # Получаем разрешения
        permissions = Permission.objects.filter(
            content_type__in=[course_content_type, lesson_content_type],
            codename__in=[
                "view_course",
                "change_course",
                "view_lesson",
                "change_lesson",
            ],
        )

        # Добавляем разрешения в группу
        moderators_group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS("Группы модераторов созданы успешно"))
