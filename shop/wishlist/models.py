from django.db import models
from product.models import Product
from accounts.models import CustomUser

class Wishlist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='user_wishlist')
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return f"Избранное {self.user.username}"