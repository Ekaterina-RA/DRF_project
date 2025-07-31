from rest_framework import serializers

from .models import Course, Lesson, Subscription
from .validators import validate_youtube


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ["owner"]
        extra_kwargs = {"video_link": {"validators": [validate_youtube]}}


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ["owner"]

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return Subscription.objects.filter(user=user, course=obj).exists()
