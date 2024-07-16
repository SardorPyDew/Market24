from rest_framework import serializers

from products.models import ProductModel
from users.models import UserModel


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = '__all__'

    """def create(self, validated_data):
        name = validated_data.get('name')
        price = validated_data.get('price')
        photo = validated_data.get('photo')
        description = validated_data.get('description')
        quantity = validated_data.get('quantity')

        user_id = UserModel.objects.filter(id=id)
        product = ProductModel.objects.create(
            name=name,
            price=price,
            photo=photo,
            description=description,
            quantity=quantity,
            user_id=user_id
        )
        return product
        # return ProductModel.objects.create(**validated_data)
"""


"""class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = 'all'"""