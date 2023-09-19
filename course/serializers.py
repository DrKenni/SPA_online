from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from course.models import Course, Lesson, Payment

MANYABLE = {'many': True, 'read_only': True}


class CourseSerializer(serializers.ModelSerializer):
    quantity_lesson = serializers.IntegerField(source='lesson_set.all.count')
    lessons = SerializerMethodField()

    def get_lessons(self, course):
        return [lesson.title for lesson in Lesson.objects.filter(course=course)]

    class Meta:
        model = Course
        fields = ('title', 'description', 'preview', 'is_published', 'quantity_lesson', 'lessons')


class LessonSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ('course', 'title', 'description', 'preview', 'video_url', 'is_published')


class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(**MANYABLE)
    lesson = LessonSerializer(**MANYABLE)

    class Meta:
        model = Payment
        fields = ('user', 'date', 'course', 'lesson', 'amount', 'method')
