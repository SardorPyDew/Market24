from django.db import models

from shared.models import BaseModel
from users.models import UserModel


class ProductModel(models.Model):

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='media')
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    # user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


