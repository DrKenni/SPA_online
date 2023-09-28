from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from course.models import Course, Lesson, Payment
from course.paginators import LessonPaginator, CoursePaginator
from course.permissions import IsOwnerOrModer, IsOwner, NotModer, IsModerator
from course.serializers import CourseSerializer, LessonSerializer, PaymentSerializer


class CourseViewSet(ModelViewSet):
    """Вывод всех действий курсов"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator
    permissions = {
        'create': NotModer,
        'retrieve': IsOwner | IsModerator,
        'list': IsAuthenticated,
        'update': IsOwner | IsModerator,
        'partial_update': IsOwner | IsModerator,
        'destroy': IsOwner
    }

    def perform_create(self, serializer):
        self.permission_classes = [NotModer]
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        self.permission_classes = [self.permissions.get(self.action)]
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    """Создание урока"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, NotModer]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Вывод списка уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPaginator
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Вывод урока по id"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Изменение урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаление урока"""
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class PaymentListAPIView(generics.ListAPIView):
    """Вывод списока платежей"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all().order_by('-id')
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'method', )
    ordering_fields = ('date', )
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    """Создание платежа"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentDetailAPIView(generics.RetrieveAPIView):
    """Вывод платежа по id"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()