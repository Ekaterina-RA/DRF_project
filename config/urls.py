from django.contrib import admin
from django.template.context_processors import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from onlinelearning.views import (
    CourseViewSet,
    LessonListCreateAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
)
from users.serializers import PaymentViewSet

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("learning/", include("onlinelearning.urls", namespace="learning")),
    path("api/", include(router.urls)),
    path("api/lessons/", LessonListCreateAPIView.as_view(), name="lesson-list"),
    path(
        "api/lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-detail"
    ),
    path(
        "api/lessons/<int:pk>/update/",
        LessonUpdateAPIView.as_view(),
        name="lesson-update",
    ),
    path(
        "api/lessons/<int:pk>/delete/",
        LessonDestroyAPIView.as_view(),
        name="lesson-delete",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
