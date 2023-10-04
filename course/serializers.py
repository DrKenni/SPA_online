from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from course.models import Course, Lesson, Payment
from course.validators import VideoURLValidator
from users.serializers import SubscriptionListSerializer

MANYABLE = {'many': True, 'read_only': True}


class CourseSerializer(serializers.ModelSerializer):
    quantity_lesson = serializers.IntegerField(source='lesson_set.all.count')
    lessons = SerializerMethodField()
    subscription = SubscriptionListSerializer(**MANYABLE)

    def get_lessons(self, course):
        return [lesson.title for lesson in Lesson.objects.filter(course=course)]

    class Meta:
        model = Course
        fields = ('title',
                  'description',
                  'preview',
                  'is_published',
                  'quantity_lesson',
                  'lessons',
                  'subscription')


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ('course',
                  'title',
                  'description',
                  'preview',
                  'video_url',
                  'is_published')

        validators = [VideoURLValidator(field='video_url'), ]


class PaymentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(**MANYABLE)

    class Meta:
        model = Payment
        fields = ('id',
                  'user',
                  'date',
                  'course',
                  'amount',
                  'method',
                  'stripe_id',
                  'stripe_status',
                  'stripe_url')
