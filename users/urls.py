from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import UsersConfig
from .views import PaymentViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns += router.urls
