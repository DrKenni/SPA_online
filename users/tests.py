from django.urls import reverse
from rest_framework import status

from course.tests import BaseTestCase
from users.models import Subscription


class SubscriptionTestCase(BaseTestCase):

    def test_create(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'course': self.course.pk,
            'user': self.user.pk,
            'is_active': True
        }
        response = self.client.post(reverse('users:subscription_create'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['course'], self.course.pk)
        # self.assertEqual(response.json().get('user'), self.user.pk)
        self.assertTrue(Subscription.objects.all().exists())
