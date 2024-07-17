from django.urls import path

from cart.views import CartAddAPIView, CartListAPIView, CartPlusAPIView

app_name = 'cart'

urlpatterns = [
    path('', CartListAPIView.as_view(), name='list'),
    path('add/', CartAddAPIView.as_view(), name='add'),
    path('plus/<int:pk>/', CartPlusAPIView.as_view(), name='plus'),
]
