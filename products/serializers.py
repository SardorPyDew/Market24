from rest_framework import serializers
from tutorial.quickstart.serializers import UserSerializer

from products.models import ProductModel
from users.models import UserModel


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = '__all__'

    # def get_me_liked(self, obj):
    #     request = self.context.get('request', None)
    #     return ProductModel.objects.filter(user_id=request.user).exists()
    # def create(self, validated_data):
    #     request = self.context.get('request', None)
    #     if request and hasattr(request, 'user'):
    #         validated_data['user_id'] = request.user
    #     return super().create(validated_data)
    #
    # def save(self, data):
    #     request = self.context.get('request', None)
    #     user_id = request.user.id
    #     return user_id


class ProductViewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductModel
        fields = ['id', 'name', 'price', 'photo', 'description', 'quantity']

