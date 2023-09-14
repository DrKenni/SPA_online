from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):

    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='course/', verbose_name='Превью', **NULLABLE)

    is_published = models.BooleanField(default=False, verbose_name='публикация')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='урок')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='course/', verbose_name='Превью', **NULLABLE)
    video_url = models.URLField(verbose_name='сылка на видео', **NULLABLE)

    is_published = models.BooleanField(default=False, verbose_name='публикация')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
