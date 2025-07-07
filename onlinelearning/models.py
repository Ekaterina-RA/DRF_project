from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255, help_text="Укажите наименование курса")
    preview = models.ImageField(upload_to="course_previews/", blank=True, null=True)
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="описание курса",
        help_text="Укажите описание курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, help_text="Укажите наименование урока")
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="описание урока",
        help_text="Укажите описание урока",
    )
    preview = models.ImageField(upload_to="lesson_previews/", blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title
