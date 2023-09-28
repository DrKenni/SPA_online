from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from course.models import NULLABLE, Course


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    city = models.CharField(max_length=150, verbose_name='город', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)

    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)
    is_active = models.BooleanField(default=False, verbose_name='активация')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Subscription(models.Model):
    is_active = models.BooleanField(default=False, verbose_name='статус подписки')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='подписчик')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='курс')

    def __str__(self):
        return f'{self.user.email} {self.course.title} '

    class Meta:
        verbose_name = 'подписчик'
        verbose_name_plural = 'подписчики'
