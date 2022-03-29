from django.contrib import admin

from orders.models import OrderModel, OrderProductModel, PaymentModel

class OrderProductInline(admin.TabularInline):
    model = OrderProductModel
    extra = 0
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'first_name', 'last_name', 'phone_number', 'email', 'city', 'order_total', 'tax', 'status', 'ip', 'is_ordered']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number','first_name', 'last_name' 'phone_number', 'email']
    list_display_links = ['first_name', 'last_name']
    list_per_page = 20
    inlines = [OrderProductInline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity','product_price', 'ordered']


# Register your models here.
admin.site.register(PaymentModel)
admin.site.register(OrderModel, OrderAdmin)
admin.site.register(OrderProductModel, OrderProductAdmin)