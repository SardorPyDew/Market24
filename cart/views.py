from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartModel
from cart.serializers import CartAddSerializer, CartListSerializer
from products.models import ProductModel
from shared.custom_pagination import CustomPagination
from shared.permission import IsOwner


class CartAddAPIView(generics.CreateAPIView):
    queryset = CartModel.objects.all()
    serializer_class = CartAddSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user_id=user)
        response = {
            'success': True,
            'message': 'Successfully added to the Cart'
        }, status
        return Response(response, status.HTTP_200_OK)


class CartListAPIView(generics.ListAPIView):
    serializer_class = CartListSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return CartModel.objects.all()


class CartPlusAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = CartAddSerializer

    def put(self, request, pk):
        print(pk)
        post = CartModel.objects.filter(product_id_id=pk).first( )
        print(post)
        if not post.exists():
            response = {
                "status": True,
                "message": "does not found",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        serializer = CartModel.objects.filter(product_id=pk)
        if serializer.is_valid():
            self.check_object_permissions(post, request)
            serializer.save(post.quantity + 1)
            response = {
                "status": True,
                "message": "Successfully updated"
            }
            return Response(response, status=status.HTTP_202_ACCEPTED)
        else:
            response = {
                "status": False,
                "message": "Invalid request",
                "error": serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)