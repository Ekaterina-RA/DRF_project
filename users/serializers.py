from rest_framework import serializers
from onlinelearning.models import Course, Lesson
from .models import Payment


class PaymentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description']  


class PaymentLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description'] 


class PaymentSerializer(serializers.ModelSerializer):
    paid_course = PaymentCourseSerializer(
        read_only=True,
        help_text="Курс оплачен"
    )
    paid_lesson = PaymentLessonSerializer(
        read_only=True,
        help_text="Урок оплачен"
    )

    def validate(self, data):
        if not data.get('paid_course') and not data.get('paid_lesson'):
            raise serializers.ValidationError("Указать либо курс, либо урок")
        if data.get('paid_course') and data.get('paid_lesson'):
            raise serializers.ValidationError(
                "Можно указать только курс или только урок"
            )
        return data

    class Meta:
        model = Payment
        fields = [
            'id', 
            'user', 
            'payment_date',
            'paid_course', 
            'paid_lesson', 
            'amount', 
            'payment_method'
        ]
        extra_kwargs = {
            'payment_date': {'read_only': True},
            'user': {'read_only': True}
        }
