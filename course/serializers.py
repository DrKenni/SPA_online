from datetime import timezone

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from course.models import Course, Lesson, Payment
from course.tasks import send_mail_about_update
from course.validators import VideoURLValidator
from users.models import Subscription
from users.serializers import SubscriptionListSerializer

MANYABLE = {'many': True, 'read_only': True}


class CourseSerializer(serializers.ModelSerializer):
    quantity_lesson = serializers.IntegerField(source='lesson_set.all.count')
    lessons = SerializerMethodField()
    subscription = SubscriptionListSerializer(**MANYABLE)

    def get_lessons(self, course):
        return [lesson.title for lesson in Lesson.objects.filter(course=course)]

    def update(self, instance, validated_data):
        sub_s = Subscription.objects.filter(course_id=instance.id, is_active=True)
        instance.updated_at = timezone.now()
        instance.save()
        if sub_s.exists():
            send_mail_about_update.delay(instance.id)
        return super().update(instance, validated_data)

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
