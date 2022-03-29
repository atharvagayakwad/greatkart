from django.db import models
from django.urls import reverse

from category.models import CategoryModel
from accounts.models import Account
from django.db.models import Avg,Count

class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    original_price = models.FloatField()
    discounted_price = models.FloatField()
    product_image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return str(self.product_name)

    def get_url(self):
        return reverse('product-detail', args=[self.category.slug, self.slug])

    def average_review(self):
        reviews = ReviewRatingModel.objects.filter(
            product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def count_reviews(self):
        reviews = ReviewRatingModel.objects.filter(
            product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            avg = int(reviews['count'])
        return count


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


class VariationModel(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return str(self.variation_value)

    class Meta:
        verbose_name = 'Variation'
        verbose_name_plural = 'Variations'


class ReviewRatingModel(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Review and Rating "
        verbose_name_plural = 'Reviews and Ratings'

    def __str__(self):
        return self.subject