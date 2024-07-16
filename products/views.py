from django.shortcuts import render
from rest_framework.permissions import IsAdminUser, IsAuthenticated
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
            product = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            response = {
                'success': False,
                'message': 'Product does not exist'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        print(product)

        product.name = request.data.get('name', product.name)
        product.price = request.data.get('price', product.price)
        product.description = request.data.get('description', product.description)
        product.quantity = request.data.get('quantity', product.quantity)
        product.save()

        response = {
            'success': True,
            'message': 'Product updated successfully'
        }
        return Response(response, status=status.HTTP_200_OK)

class UserProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return ProductModel.objects.all()


class ProductsDetailView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        product_id = self.kwargs.get('pk')
        return ProductModel.objects.filter(id=product_id)




