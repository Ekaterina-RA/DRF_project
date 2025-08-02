from django.urls import include, path
from rest_framework.routers import SimpleRouter

from onlinelearning.apps import OnlinelearningConfig
from onlinelearning.views import (CourseViewSet, LessonViewSet,
                                  SubscriptionAPIView)
from users.views import PaymentViewSet

app_name = OnlinelearningConfig.name

router = SimpleRouter()
router.register(r"courses", CourseViewSet, basename="courses")
router.register(r"lessons", LessonViewSet, basename="lessons")
router.register(r"api/payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path("", include(router.urls)),
    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscriptions"),
]

urlpatterns += router.urls
