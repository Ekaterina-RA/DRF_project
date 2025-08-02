from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from config import settings
from onlinelearning.views import CourseViewSet, home
from users.views import CustomTokenObtainPairView, PaymentViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Online Learning API",
        default_version="v1",
        description="Документация для платформы онлайн-обучения",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


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
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
