from django.urls import include, path
from rest_framework.routers import SimpleRouter

from onlinelearning.apps import OnlinelearningConfig
from onlinelearning.views import CourseViewSet, LessonViewSet

app_name = OnlinelearningConfig.name

router = SimpleRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"lessons", LessonViewSet, basename="lesson")

urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns += router.urls
