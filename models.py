from django.db import models
from django.contrib.auth.models import User

# Cart model to store user's cart items
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    items = models.JSONField(default=dict)  # Use JSONField to store items and quantities

    def __str__(self):
        return f"Cart of {self.user.username}"

# Product model to store product data including metadata from style.csv
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()  # Or use an ImageField for locally stored images

    # Additional fields to store metadata from style.csv
    gender = models.CharField(max_length=20)
    masterCategory = models.CharField(max_length=50)
    subCategory = models.CharField(max_length=50)
    articleType = models.CharField(max_length=50)
    baseColour = models.CharField(max_length=20)
    season = models.CharField(max_length=20)
    year = models.IntegerField()
    usage = models.CharField(max_length=20)
    productDisplayName = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Recommendation model to store user-specific image recommendations
class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommendations")
    image_name = models.CharField(max_length=255)  # Store recommended image filename
    uploaded_image = models.ImageField(upload_to='uploads/')  # Store uploaded image
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"Recommendation for {self.user.username}: {self.image_name}"
