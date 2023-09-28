from django.urls import path
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserViewSet, SubscriptionCreateAPIView, SubscriptionDeleteAPIView

app_name = UsersConfig.name


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    #Подписка
    path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('subscription/delete/<int:pk>/', SubscriptionDeleteAPIView.as_view(), name='subscription_delete'),

    # Токен
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
