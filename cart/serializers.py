from rest_framework import serializers
from rest_framework.permissions import IsAdminUser

from cart.models import CartModel
from products.models import ProductModel
from products.serializers import ProductSerializer


class CartAddSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, source='product_id')

    class Meta:
        model = CartModel
        fields = ['product_id', 'quantity']

    def create(self, validated_data):
        return super().create(validated_data)


class CartListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, source='product_id')

    class Meta:
        model = CartModel
        fields = ['product', 'quantity']

    def validate(self, data):
        story_id = self.request.data['product_id']
        ProductModel.objects.filter(user=self.request.user, id=story_id)
