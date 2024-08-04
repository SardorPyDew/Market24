from django.db import models

from products.models import ProductModel
from users.models import UserModel


class CartModel(models.Model):
    product_id = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='carts')
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='users')
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class Cart(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.ProductModel', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
