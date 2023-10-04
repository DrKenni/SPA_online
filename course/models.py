from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):

    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='course/', verbose_name='Превью', **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='публикация')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)
    title = models.CharField(max_length=150, verbose_name='урок')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='course/', verbose_name='Превью', **NULLABLE)
    video_url = models.URLField(verbose_name='сылка на видео', **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='публикация')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    CASH = 'CASH'
    TRANSFER = 'TRANSFER'

    PAYMENT_METHOD_CHOICES = [
        (CASH, 'Наличные'),
        (TRANSFER, 'Перевод'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='Пользователь', **NULLABLE,)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)

    amount = models.IntegerField(verbose_name='сумма оплаты')
    method = models.CharField(max_length=8, choices=PAYMENT_METHOD_CHOICES, verbose_name='способ оплаты', **NULLABLE,)
    date = models.DateField(auto_now_add=True, verbose_name='Дата оплаты')
    stripe_id = models.CharField(max_length=300, verbose_name='id оплаты в stripe', **NULLABLE)
    stripe_status = models.CharField(max_length=15, default='open', verbose_name='статус')
    stripe_url = models.TextField(verbose_name='url на платеж', **NULLABLE)

    def __str__(self):
        return f'{self.method}: {self.amount} - {self.date}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('-course', '-date', '-method')
