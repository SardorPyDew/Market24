from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartModel
from cart.serializers import CartAddSerializer
from products.models import ProductModel
from shared.custom_pagination import CustomPagination


class CartAddAPIView(generics.CreateAPIView):
    queryset = CartModel.objects.all()
    serializer_class = CartAddSerializer
    permission_classes = [IsAdminUser]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    # def perform_create(self, serializer):
    #     if serializer.is_valid():
    #         print(serializer.validated_data)
    #     get_id = self.kwargs.get('pk')
    #     serializer.save(user_id=get_id)
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user_id=user)
        response = {
            'success': True,
            'message': 'Successfully added to the Cart'
        }, status
        return Response(response, status.HTTP_200_OK)


class CartListAPIView(generics.ListAPIView):
    serializer_class = CartAddSerializer
    permission_classes = [IsAdminUser]

    # def get_queryset(self):
    #     user = self.request.user
    #     return CartModel.objects.filter(user=user)

    def get_queryset(self):
        carts = CartModel.objects.all()  # Barcha savat elementlarini olish
        product_ids = [cart.product_id for cart in carts]  # Savat elementlarining product_id larini olish
        pr_id = CartModel.objects.g

        products = ProductModel.objects.filter(id=product_ids)
        return products
