from datetime import timedelta
from smtplib import SMTPException

from django.utils import timezone

from django.core.mail import send_mail

from celery import shared_task

from config import settings
from course.models import Course
from users.models import User, Subscription


@shared_task
def send_mail_about_update(course_id):
    try:
        course = Course.objects.get(pk=course_id)
        subscriptions = Subscription.objects.filter(course=course, is_active=True)

        email_list = [subscription.user.email for subscription in subscriptions]
        subject = f'Обновился курса {course.title}'
        message = f'Курс обновился'
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(subject, message, from_email, email_list, fail_silently=False)
    except SMTPException as er:
        print(f'Произошла ошибка при отправке письма: {er}')


@shared_task
def check_last_login():
    try:
        users = User.objects.all()
        month = timedelta(days=30)
        for user in users:
            if timezone.now() - user.last_login > month:
                user.is_active = False
                user.save()
    except Exception as e:
        return f'Произошла ошибка: {str(e)}'
