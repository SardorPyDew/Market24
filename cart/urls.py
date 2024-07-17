from django.urls import path

from cart.views import CartAddAPIView, CartListAPIView

app_name = 'cart'

urlpatterns = [
    path('', CartListAPIView.as_view(), name='list'),
    path('add/', CartAddAPIView.as_view(), name='add'),
]
