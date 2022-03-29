from django.contrib import admin

from store.models import Product, VariationModel,ReviewRatingModel


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'original_price', 'discounted_price', 'stock', 'category', 'created_date', 'modified_date', 'is_available')
    prepopulated_fields = {'slug':('product_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'created_date', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'review', 'rating', 'status', 'created_at')

admin.site.register(Product, ProductAdmin)
admin.site.register(VariationModel, VariationAdmin)
admin.site.register(ReviewRatingModel)