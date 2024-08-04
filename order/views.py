from django.shortcuts import render
from rest_framework import permissions, generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from order.models import OrderModel
from order.serializers import OrderSerializer
from shared.custom_pagination import CustomPagination


# Create your views here.
class UserOrdersAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return OrderModel.objects.filter(user_id=user_id)


class OrderUpdateAPIView(generics.UpdateAPIView):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        order_id = self.kwargs.get('pk')
        try:
            return self.queryset.get(id=order_id)
        except OrderModel.DoesNotExist:
            raise NotFound(detail="Order not found")

    def put(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": f"Order status updated to ---> {serializer.data['status']}."},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderDetailView(generics.RetrieveAPIView):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class OrderDeleteAPIView(generics.DestroyAPIView):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        order_id = self.kwargs.get('pk')
        try:
            return self.queryset.get(id=order_id)
        except OrderModel.DoesNotExist:
            raise NotFound(detail="Order not found")

    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        order.delete()
        return Response({"detail": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
