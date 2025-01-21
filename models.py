
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=255)  # Store image as number (e.g., '1163.jpg')

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    imagename = models.CharField(max_length=255, default='default_image.jpg')  # Default value for new rows

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
class CartItem(models.Model):
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product_name