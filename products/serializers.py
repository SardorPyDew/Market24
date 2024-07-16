from rest_framework import serializers
from tutorial.quickstart.serializers import UserSerializer

from products.models import ProductModel
from users.models import UserModel


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = '__all__'


class ProductViewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductModel
        fields = ['id', 'name', 'price', 'photo', 'description', 'quantity']

