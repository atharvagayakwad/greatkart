from django.db import models
from django.urls import reverse

# Create your models here.
class CategoryModel(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    category_image = models.ImageField(upload_to="photos/categories", blank=True)


    def __str__(self):
        return str(self.category_name)

    def get_url(self):
        return reverse('products-by-category', args=[self.slug])

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'