from rest_framework import serializers
from .models import Course, Lesson


class LessonListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка уроков"""
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'video_link']


class LessonDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра урока"""
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonListSerializer(
        source='lessons.all', 
        many=True, 
        read_only=True,
        help_text="Список уроков курса"
    )
    lesson_count = serializers.SerializerMethodField(
        help_text="Количество уроков в курсе"
    )

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'lesson_count', 'lessons']
        extra_kwargs = {
            'preview': {'read_only': True}
        }

    def get_lesson_count(self, obj):
        return obj.lessons.count()
