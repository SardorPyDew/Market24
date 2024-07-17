from django.urls import path

from products.views import ProductCreateAPIView, UserProductListView, ProductsDetailView, ProductsUpdateView, \
    ProductDeleteView

app_name = 'products'

urlpatterns = [
    path('add/', ProductCreateAPIView.as_view(), name='add'),
    path('list/', UserProductListView.as_view(), name='list'),
    path('update/<int:pk>/', ProductsUpdateView.as_view(), name='update'),
    path('<int:pk>/detail/', ProductsDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='delete'),
]


