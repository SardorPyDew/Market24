from django.db import models

from products.models import ProductModel
from users.models import UserModel


class CartModel(models.Model):
    product_id = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='carts')
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='users')
    quantity = models.IntegerField()

    def __str__(self):
        return self.quantity

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

