from django.db import models
from orders.models import Order
from accounts.models import CustomUser

class OrderStatus(models.Model):
    STATUS_NEW = 'new'
    STATUS_PROCESSING = 'processing'
    STATUS_DONE = 'done'
    STATUS_CHOICES = [
        (STATUS_NEW,'Новый'),
        (STATUS_PROCESSING,'На сборке'),
        (STATUS_DONE,'Собран'),
    ]

    order = models.OneToOneField(Order,on_delete=models.CASCADE, related_name='order',
                              verbose_name='Заказ')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW,
                              verbose_name='Статус заказа')
    picker = models.ForeignKey(CustomUser,on_delete=models.SET_NULL, null=True,
                               blank=True, related_name='picker')
    picked = models.DateTimeField(null=True, blank=True, verbose_name='Время сборки')