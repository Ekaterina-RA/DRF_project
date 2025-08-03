from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from onlinelearning.models import Course
from onlinelearning.services_stripe import StripeService

from .models import Payment, User
from .permissions import IsOwner
from .serializers import (CustomTokenObtainPairSerializer, GroupSerializer,
                          PaymentSerializer, UserProfileSerializer,
                          UserRegisterSerializer)


class PaymentViewSet(viewsets.ModelViewSet):
    """Класс для работы с платежами через Stripe"""

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

    @swagger_auto_schema(
        method="post",
        operation_summary="Создать платеж",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["course_id"],
            properties={
                "course_id": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={
            201: openapi.Response(
                description="Ссылка на оплату",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "payment_url": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: "Неверные данные",
            404: "Курс не найден",
        },
    )
    @action(detail=False, methods=["post"], url_path="create")
    def create_payment(self, request):
        course = get_object_or_404(Course, id=request.data.get("course_id"))
        amount = request.data.get("amount")

        # Создаем продукт и цену в Stripe
        product_id = StripeService.create_product(
            name=course.title, description=course.description
        )
        price_id = StripeService.create_price(
            amount=float(amount), product_id=product_id
        )

        # Создаем сессию оплаты
        session = StripeService.create_session(
            price_id=price_id,
            success_url="http://127.0.0.1:8000/success/",
            cancel_url="http://127.0.0.1:8000/cancel/",
        )

        # Сохраняем платеж в БД
        payment = Payment.objects.create(
            user=request.user,
            paid_course=course,
            amount=float(amount),
            stripe_product_id=product_id,
            stripe_price_id=price_id,
            stripe_session_id=session["session_id"],
            stripe_payment_url=session["payment_url"],
        )

        return Response(
            {"payment_url": session["payment_url"]}, status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        method="get",
        operation_summary="Проверить статус платежа",
        responses={
            200: openapi.Response(
                description="Статус платежа",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "is_paid": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    },
                ),
            ),
            404: "Платеж не найден",
        },
    )
    @action(detail=True, methods=["get"], url_path="check-status")
    def check_status(self, request, pk=None):
        """Проверка статуса платежа в Stripe"""
        payment = get_object_or_404(Payment, id=pk, user=request.user)
        is_paid = StripeService.check_payment_status(payment.stripe_session_id)

        if is_paid and not payment.is_paid:
            payment.is_paid = True
            payment.save()

        return Response({"is_paid": is_paid})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegisterSerializer
        return UserProfileSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(id=self.request.user.id)
        return queryset

    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
