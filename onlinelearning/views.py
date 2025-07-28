from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson
from .permissions import IsModerator, IsOwnerOrModerator
from .serializers import CourseSerializer, LessonSerializer


def home(request):
    return HttpResponse("Добро пожаловать на онлайн-обучение!")


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff and not IsModerator().has_permission(
            self.request, self
        ):
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()  # Добавляем базовый queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff and not IsModerator().has_permission(
            self.request, self
        ):
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
