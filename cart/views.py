from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartModel, Cart, CartItem
from cart.serializers import CartAddSerializer, CartListSerializer, CheckoutSerializer
from order.models import OrderModel, OrderItem
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

    def put(self, request, pk):
        try:
            # product_id ga ko'ra birinchi cart elementni topish
            post = CartModel.objects.get(product_id=pk, user=request.user)
        except CartModel.DoesNotExist:
            response = {
                "status": False,
                "message": "Product not found in cart.",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        # Miqdorni oshirish
        post.quantity += 1
        post.save()

        serializer = CartAddSerializer(post)
        response = {
            "status": True,
            "message": "Successfully updated",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_202_ACCEPTED)


class CheckoutAPIView(generics.CreateAPIView):
    queryset = OrderModel.objects.all()
    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            cart_id = serializer.validated_data.get('cart_id')
            phone_number = serializer.validated_data.get('phone_number')
            address = serializer.validated_data.get('address')

            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                return Response({"detail": f"Cart with id {cart_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

            order = OrderModel.objects.create(
                user=request.user,
                phone_number=phone_number,
                address=address,
                cart=cart
            )

            cart_items = CartItem.objects.filter(cart=cart)
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity
                )

            cart_items.delete()

            return Response({"status": True, "detail": "Order created successfully!..."},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
