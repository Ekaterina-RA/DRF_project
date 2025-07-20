from django.core.management.base import BaseCommand
from users.models import Payment, User
from onlinelearning.models import Course, Lesson


class Command(BaseCommand):
    help = "Load payments data"

    def handle(self, *args, **options):
        user1 = User.objects.get(email="user1@example.com")
        user2 = User.objects.get(email="user2@example.com")
        course1 = Course.objects.get(title="Course 1")
        lesson1 = Lesson.objects.get(title="Lesson 1")

        Payment.objects.create(
            user=user1,
            paid_course=course1,
            paid_lesson=None,
            amount=1000.00,
            payment_method="transfer",
        )

        Payment.objects.create(
            user=user2,
            paid_course=None,
            paid_lesson=lesson1,
            amount=500.00,
            payment_method="cash",
        )

        self.stdout.write(self.style.SUCCESS("Successfully loaded payments data"))
