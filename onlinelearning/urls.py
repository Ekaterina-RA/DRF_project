from django.urls import include, path
from rest_framework.routers import SimpleRouter

from onlinelearning.apps import OnlinelearningConfig
from onlinelearning.views import (CourseViewSet, LessonDestroyAPIView,
                                  LessonListCreateAPIView,
                                  LessonRetrieveAPIView, LessonUpdateAPIView,
                                  LessonViewSet)

app_name = OnlinelearningConfig.name

router = SimpleRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"lessons", LessonViewSet, basename="lesson")

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListCreateAPIView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path(
        "lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"
    ),
    path(
        "lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_delete"
    ),
]

urlpatterns += router.urls
