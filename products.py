from django.db import models

class Product(models.Model):
    # Product name
    name = models.CharField(max_length=255)
    
    # Product description
    description = models.TextField()
    
    # Price of the product
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Example: 99999.99
    
    # Product image (optional)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # Stock of the product (how many units available)
    stock = models.PositiveIntegerField(default=0)
    
    # Timestamp for when the product was added or last modified
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
