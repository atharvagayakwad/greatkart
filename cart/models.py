from django.db import models
from accounts.models import Account

from store.models import Product
from django.contrib.auth.models import User
from store.models import VariationModel

# Create your models here.
class CartModel(models.Model):
    cart_id = models.CharField(max_length=255, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'

    def __str__(self):
        return self.cart_id

class CartItemModel(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(VariationModel, blank=True)
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def __unicode__(self):
        return self.product

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    