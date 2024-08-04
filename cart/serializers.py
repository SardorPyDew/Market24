from rest_framework import serializers
from rest_framework.permissions import IsAdminUser

from cart.models import CartModel, Cart, CartItem
from order.models import OrderModel, OrderItem
from products.models import ProductModel
from products.serializers import ProductSerializer


class CartAddSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, source='product_id')

    class Meta:
        model = CartModel
        fields = ['product', 'product_id', 'quantity']

    def validate_product_id(self, value):
        if not ProductModel.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product with this ID does not exist.")
        return value

    def create(self, validated_data):
        return super().create(validated_data)


class CartListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, source='product_id')

    class Meta:
        model = CartModel
        fields = '__all__'

    def validate(self, data):
        story_id = self.request.data['product_id']
        ProductModel.objects.filter(user=self.request.user, id=story_id)


class CheckoutSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=255)

    def validate_cart_id(self, value):
        try:
            cart = Cart.objects.get(id=value)
        except Cart.DoesNotExist:
            raise serializers.ValidationError(f"Cart with id {value} does not exist.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        cart_id = validated_data['cart_id']
        phone_number = validated_data['phone_number']
        address = validated_data['address']

        cart = Cart.objects.get(id=cart_id)

        order = OrderModel.objects.create(
            user=user,
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

        return order
