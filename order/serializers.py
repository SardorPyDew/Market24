from rest_framework import serializers

from order.models import OrderModel, OrderProductModel
from products.serializers import ProductSerializer


class OrderProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderProductModel
        fields = ['product', 'product_id', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = OrderModel
        fields = ['id', 'items', 'status', 'phone_number', 'address', 'created_at']
