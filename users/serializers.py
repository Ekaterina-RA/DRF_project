from rest_framework import serializers, viewsets
from onlinelearning.serializers import CourseSerializer, LessonSerializer
from .models import Payment
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class PaymentSerializer(serializers.ModelSerializer):
    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
