from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        "paid_course": ["exact", "isnull"],
        "paid_lesson": ["exact", "isnull"],
        "payment_method": ["exact"],
        "payment_date": ["gte", "lte", "exact"],
        "amount": ["gte", "lte", "exact"],
    }
    ordering_fields = ["payment_date", "amount"]
    ordering = ["-payment_date"]  # Сортировка по умолчанию

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset
