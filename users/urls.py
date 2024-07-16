from django.urls import path
from users.views import *


app_name = 'users'

urlpatterns = [
    path('register/', RegisterCreateAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/', UserVerifyCodeAPIView.as_view(), name='verify'),
    path('update/', UserUpdateAPIView.as_view(), name='update'),
    path('resend/code/', ResendVerifyCodeAPIView.as_view(), name='resend-code'),
    path('password/forget/', ForgetPasswordView.as_view(), name='resend-code'),
    path('refresh/token/', RefreshTokenView.as_view(), name='refresh-token'),

    # Users all Admin
    path('list/', LoginListAPIView.as_view(), name='login-list'),
    path('<int:pk>/', UserDetailAPIView.as_view(), name='user-detail')
]

