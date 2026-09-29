from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import UserCreateAPIView,RetrieveUpdateDestroyAPIView, PasswordResetAPIView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create/', UserCreateAPIView.as_view(), name='user_create'),
    path('me/',RetrieveUpdateDestroyAPIView.as_view(),name='user_me'),
    path('me/password/',PasswordResetAPIView.as_view(),name='user_password')
]