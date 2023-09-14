
from django.urls import path

from rest_framework.routers import DefaultRouter

from course.apps import CourseConfig
from course.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

app_name = CourseConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='create'),
    path('lesson/', LessonListAPIView.as_view(), name='list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='delete'),
] + router.urls
