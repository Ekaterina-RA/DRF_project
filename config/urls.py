from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from config import settings
from onlinelearning.views import CourseViewSet, home
from users.views import CustomTokenObtainPairView, PaymentViewSet

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"users", PaymentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),
    path("learning/", include("onlinelearning.urls", namespace="learning")),
    path("users/", include("users.urls", namespace="users")),
    path("api/payments/", include("users.urls")),
    path("api/", include(router.urls)),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="api_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/users/", include("users.urls")),
    path("api/", include("onlinelearning.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
