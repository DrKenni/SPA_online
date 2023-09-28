from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from course.models import Course, Lesson
from users.models import User


class BaseTestCase(APITestCase):
    email = 'test1@test.com'
    password = 'qwer1234'

    def setUp(self) -> None:
        self.user = User.objects.create(email=self.email)
        self.user.set_password(self.password)
        self.user.save()
        get_token = reverse('users:token_obtain_pair')
        response = self.client.post(path=get_token, data={'email': self.email,
                                                          'password': self.password})

        self.token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        self.course = Course.objects.create(title='test_course')


class LessonTestCase(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.lesson = Lesson.objects.create(
            title='test',
            course=self.course,
            description='test description',
            video_url='url',
            owner=self.user
        )

    def test_create(self):
        data = {
            "title": "test",
            "course": 1,
            "video_url": "https://youtube.com"
        }
        self.client.force_authenticate(user=self.user)
        create_lesson = reverse('course:create')
        response = self.client.post(path=create_lesson, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], data['title'])
        self.assertTrue(Lesson.objects.all().exists)

    def test_create_validator(self):
        data = {
            "title": "test",
            "course": self.lesson.course_id,
            "video_url": "https://vk.com"
        }
        self.client.force_authenticate(user=self.user)
        create_lesson = reverse('course:create')
        response = self.client.post(path=create_lesson, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors':
                                               ['Можно вставить только видео с YouTube.com']}
                         )
        self.assertTrue(Lesson.objects.all().exists())

    def test_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('course:list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'count': 1,
                          'next': None,
                          'previous': None,
                          'results': [
                              {'course': self.lesson.course_id,
                               'title': self.lesson.title,
                               'description': self.lesson.description,
                               'preview': self.lesson.preview,
                               'video_url': self.lesson.video_url,
                               'is_published': self.lesson.is_published
                               }
                          ]
                          }
                         )
        self.assertTrue(Lesson.objects.all().exists)

    def test_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/lesson/{self.lesson.pk}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'course': self.lesson.course_id,
                          'title': self.lesson.title,
                          'description': self.lesson.description,
                          'preview': self.lesson.preview,
                          'video_url': self.lesson.video_url,
                          'is_published': self.lesson.is_published})
        self.assertTrue(Lesson.objects.all().exists())

    def test_update(self):
        data = {
            'title': 'update title',
            'description': 'update description',
        }
        self.client.force_authenticate(user=self.user)
        update_path = reverse('course:update', kwargs={'pk': self.lesson.pk})
        response = self.client.patch(path=update_path, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Lesson.objects.all().exists())

    def test_delete(self):
        self.client.force_authenticate(user=self.user)
        delete_path = reverse('course:delete', kwargs={'pk': self.lesson.pk})
        response = self.client.delete(path=delete_path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.all().exists())

    def tearDown(self) -> None:
        self.user.delete()
        self.course.delete()
        self.lesson.delete()
