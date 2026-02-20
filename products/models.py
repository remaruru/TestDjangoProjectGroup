from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="FontAwesome class or similar")

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="URL needed for demo purposes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Simple stock management
    stock = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
