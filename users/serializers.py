from rest_framework import serializers
from onlinelearning.models import Course, Lesson
from .models import Payment


class SimpleCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title"]


class SimpleLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title"]


class PaymentSerializer(serializers.ModelSerializer):
    paid_course = SimpleCourseSerializer(read_only=True)
    paid_lesson = SimpleLessonSerializer(read_only=True)

    def validate(self, data):
        if not data.get("paid_course") and not data.get("paid_lesson"):
            raise serializers.ValidationError("Должен быть указан либо курс, либо урок")
        if data.get("paid_course") and data.get("paid_lesson"):
            raise serializers.ValidationError(
                "Можно указать только курс или только урок"
            )
        return data

    class Meta:
        model = Payment
        fields = ["id", "user", "paid_course", "paid_lesson", "amount", "payment_date"]
        ordering = ["-payment_date"]
