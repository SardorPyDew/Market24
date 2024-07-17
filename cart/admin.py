from django.contrib import admin

from cart.models import CartModel


@admin.register(CartModel)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'quantity', 'user_id',)
    search_fields = ('created_at',)
    list_filter = ('user_id',)
