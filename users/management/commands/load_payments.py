from django.core.management.base import BaseCommand
from users.models import User
from onlinelearning.models import Course, Lesson
from users.models import Payment
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Fill payments with test data"

    def handle(self, *args, **options):
        users = User.objects.all()
        courses = Course.objects.all()
        lessons = Lesson.objects.all()
        payment_methods = ["cash", "transfer"]

        for i in range(20):
            user = random.choice(users)
            payment_date = datetime.now() - timedelta(days=random.randint(1, 30))

            # Выбираем случайно курс или урок
            if random.choice([True, False]):
                paid_course = random.choice(courses)
                paid_lesson = None
                amount = random.randint(1000, 5000)
            else:
                paid_course = None
                paid_lesson = random.choice(lessons)
                amount = random.randint(500, 2000)

            payment = Payment(
                user=user,
                payment_date=payment_date,
                paid_course=paid_course,
                paid_lesson=paid_lesson,
                amount=amount,
                payment_method=random.choice(payment_methods),
            )
            payment.save()

        self.stdout.write(self.style.SUCCESS("Successfully filled payments"))
