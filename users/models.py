from django.contrib.auth.models import AbstractUser
from django.db import models

from course.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    city = models.CharField(max_length=150, verbose_name='город', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)

    is_active = models.BooleanField(default=False, verbose_name='активаия')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []