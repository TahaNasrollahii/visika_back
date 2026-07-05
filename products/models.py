from django.db import models
from core.models import TimestampedModel

class Category(TimestampedModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

class Product(TimestampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    badge = models.CharField(max_length=50, blank=True)
    is_best_seller = models.BooleanField(default=False)
    is_hot_offer = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def image(self):
        first_image = self.images.first()
        if first_image and first_image.image:
            return first_image.image.url
        return None

class ProductImage(TimestampedModel):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.title}"

class ProductFeature(TimestampedModel):
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.title}: {self.value}"
