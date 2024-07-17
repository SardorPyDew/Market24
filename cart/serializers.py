from rest_framework import serializers

from cart.models import CartModel
from products.models import ProductModel
from products.serializers import ProductSerializer


class CartAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartModel
        fields = ['product_id', 'quantity']

    def create(self, validated_data):
        return super().create(validated_data)

    # def get_me_liked(self, obj):
    #     request = self.context.get('request', None)
    #     return CartModel.objects.filter(post=obj.product_id, user=request.user).exists()


class CartListSerializer(serializers.ModelSerializer):
    product = CartAddSerializer(read_only=True)

    class Meta:
        model = CartModel
        fields = ['id', 'name', 'price', 'photo', 'description', 'quantity']
