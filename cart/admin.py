from django.contrib import admin

from cart.models import CartItemModel, CartModel


class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')
    list_editable = ('is_active',)

# Register your models here.
admin.site.register(CartModel,CartAdmin)
admin.site.register(CartItemModel,CartItemAdmin)