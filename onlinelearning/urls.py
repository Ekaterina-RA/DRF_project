from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import CourseViewSet, LessonListCreateAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, LessonDestroyAPIView
from onlinelearning.apps import OnlinelearningConfig

app_name = OnlinelearningConfig.name

router = SimpleRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson_list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
]

urlpatterns += router.urls