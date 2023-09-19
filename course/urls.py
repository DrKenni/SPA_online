
from django.urls import path

from rest_framework.routers import DefaultRouter

from course.apps import CourseConfig
from course.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, PaymentCreateAPIView, PaymentDetailAPIView

app_name = CourseConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    # Lesson
    path('lesson/create/', LessonCreateAPIView.as_view(), name='create'),
    path('lesson/', LessonListAPIView.as_view(), name='list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='delete'),

    # Payment
    path('payment/', PaymentListAPIView.as_view(), name='list_payment'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='create_payment'),
    path('payment/<int:pk>/', PaymentDetailAPIView.as_view(), name='get_payment'),
] + router.urls
