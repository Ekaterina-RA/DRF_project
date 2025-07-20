from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lessons.count()