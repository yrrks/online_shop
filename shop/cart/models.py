from django.db import models
from accounts.models import CustomUser
from product.models import Product


class Cart(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,
                                related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,
                             related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['cart', 'product']

    def total_price(self):
        return self.quantity * self.product.price