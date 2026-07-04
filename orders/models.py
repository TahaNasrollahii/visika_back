from django.db import models
from django.contrib.auth import get_user_model
from core.models import TimestampedModel
from products.models import Product

User = get_user_model()

class Cart(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart for {self.user.phone_number}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(TimestampedModel):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    @property
    def total_price(self):
        price = self.product.discount_price if self.product.discount_price else self.product.price
        return price * self.quantity

class Order(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=50, default='pending')
    total_amount = models.PositiveIntegerField()

    def __str__(self):
        return f"Order #{self.id} by {self.user.phone_number}"

class OrderItem(TimestampedModel):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField() # Price at the time of order

    def __str__(self):
        return f"{self.quantity} x {self.product.title if self.product else 'Deleted'}"
