from django.contrib import admin

from products.models import ProductModel


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'created_at',)
    search_fields = ('name', 'created_at')
    list_filter = ('created_at', 'updated_at',)
