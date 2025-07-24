from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Payment, User
from .serializers import (CustomTokenObtainPairSerializer, PaymentSerializer,
                          UserSerializer)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        "paid_course": ["exact", "isnull"],
        "paid_lesson": ["exact", "isnull"],
        "payment_method": ["exact"],
        "payment_date": ["gte", "lte", "exact"],
        "amount": ["gte", "lte", "exact"],
    }
    ordering_fields = ["payment_date", "amount"]
    ordering = ["-payment_date"]

    def get_extra_action_map(self):
        return {}

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
