from django.urls import include, path
from rest_framework.routers import SimpleRouter

from onlinelearning.apps import OnlinelearningConfig
from onlinelearning.views import CourseViewSet, LessonViewSet, SubscriptionAPIView

app_name = OnlinelearningConfig.name

router = SimpleRouter()
router.register(r"courses", CourseViewSet, basename="courses")
router.register(r"lessons", LessonViewSet, basename="lessons")

urlpatterns = [
    path("", include(router.urls)),
    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscriptions"),
]

urlpatterns += router.urls
