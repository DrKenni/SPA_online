from django.core.management import BaseCommand

from course.models import Lesson, Payment, Course


class Command(BaseCommand):

    def handle(self, *args, **options) -> None:

        Course.objects.all().delete()
        Lesson.objects.all().delete()
        Payment.objects.all().delete()

        # Курс
        course_list = [
            {'id': 1, 'title': 'SkyPro', 'description': 'Информативно и позновательно'},
            {'id': 2, 'title': 'Горный', 'description': 'У нас тут темно'},
            {'id': 3, 'title': 'Школьный', 'description': 'Для начинающих жизнь'},
        ]

        course_for_create = []

        for course_item in course_list:
            course_for_create.append(
                Course(**course_item)
            )
        Course.objects.bulk_create(course_for_create)

        # Урок
        lesson_list = [
            {'id': 1, 'title': 'Математика', 'description': '2+2=4', "course": Course.objects.get(pk=3)},
            {'id': 2, 'title': 'Чтение', 'description': 'Тут ты научишься читать', "course": Course.objects.get(pk=3)},
            {'id': 3, 'title': 'Геодезия', 'description': 'Проломи землю головой', "course": Course.objects.get(pk=2)},
            {'id': 4, 'title': 'Django', 'description': 'Создание сайтов', 'course': Course.objects.get(pk=1)},
            {'id': 5, 'title': 'Python', 'description': 'Научимся разговаривать на языке цифр', 'course': Course.objects.get(pk=1)},
            {'id': 6, 'title': 'Сейсмология', 'description': 'i am Earth Shaker', 'course': Course.objects.get(pk=2)},
            {'id': 7, 'title': 'Информатика', 'description': 'Я робот', 'course': Course.objects.get(pk=1)},
        ]

        lesson_for_create = []
        for lesson_item in lesson_list:
            lesson_for_create.append(
                Lesson(**lesson_item)
            )
        Lesson.objects.bulk_create(lesson_for_create)

        # Платеж
        payment_list = [
            {'id': 1, 'amount': 700, 'method': Payment.TRANSFER},
            {'id': 2, 'amount': 500, 'method': Payment.CASH},
            {'id': 3, 'amount': 650, 'method': Payment.CASH},
            {'id': 4, 'amount': 1000, 'method': Payment.TRANSFER},
        ]

        payment_for_create = []
        for payment_item in payment_list:
            payment_for_create.append(
                Payment(**payment_item)
            )
        Payment.objects.bulk_create(payment_for_create)
