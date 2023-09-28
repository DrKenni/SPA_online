from rest_framework import serializers

from course.models import Course
from users.models import User, Subscription


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = ('is_active', 'course', 'user')


class SubscriptionListSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Subscription
        fields = ('is_active', 'course', 'user')