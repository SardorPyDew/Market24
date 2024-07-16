from django.shortcuts import render
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from products.models import ProductModel
from products.serializers import ProductSerializer
from shared.custom_pagination import CustomPagination
from users.models import UserModel


class ProductCreateAPIView(generics.CreateAPIView):
    model = ProductModel.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination

    # def post(self, request, *args, **kwargs):
    #    user_id = ProductModel.objects.all()
    #    user_id = UserModel.objects.filter(id=user_id.user_)


class ProductsUpdateView(generics.UpdateAPIView):
    queryset = ProductModel.objects.all()
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        product_id = kwargs['pk']
        try:
            product_id = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            response = {
                'success': False,
                'message': 'Product does not exist'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        ProductModel.objects.update(
            name=request.data['name'],
            price=request.data['price'],
            description=request.data['description'],
            quantity=request.data['quantity']
        )
        response = {
            'success': True,
            'message': 'Product updated successfully'
        }
        return Response(response, status=status.HTTP_201_CREATED)