from django.db import models
from mptt.models import MPTTModel,TreeForeignKey
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.urls import reverse


class Category(MPTTModel):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Url')
    parent = TreeForeignKey('self',on_delete=models.CASCADE, null=True, blank=True,
                               related_name='child', verbose_name='Родительская категория')
    description = models.TextField(blank=True, verbose_name='Описании категории')
    #image = models.ImageField(upload_to='categories/', blank=True,
    #                           verbose_name='Изображение категории')
    is_active = models.BooleanField(default=True, verbose_name='Активность')

    class MPTTMeta:
        order_insertion_by = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:product_list_by_category', args=[self.slug])


class Product(models.Model):

    name = models.CharField(max_length=100, verbose_name='Название товара')
    slug = models.SlugField(max_length=100, verbose_name='Url')
    category = models.ForeignKey(Category,on_delete=models.PROTECT,
                                related_name='products',verbose_name='Категория')
    price = models.DecimalField(max_digits=8, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.01'))],
                                verbose_name='Цена')
    #old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
    #                            null=True,validators=[MinValueValidator(Decimal('0.00'))],
    #                            verbose_name='Старая цена')
    quantity = models.PositiveIntegerField(default=0,verbose_name='Количество на складе')

    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True,
                                   verbose_name='Главное изображение')

    description = models.TextField(max_length=200, blank=True,
                                verbose_name='Описание товара')
    specifications = models.JSONField(default=dict,blank=True,
                                verbose_name='Характеристики товара',
                                help_text='Данные JSON: {"название":"значение"}')
    available = models.BooleanField(default=True,verbose_name='Активен')
    created = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True,verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = [
            #'-is_active',
            '-created']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:product_detail', args=[self.id, self.slug])

    @property
    def in_stock(self):
        return self.quantity > 0

    #@property
    #def discount(self):
    #    if self.old_price and self.old_price > self.price:
    #        return  round((1- self.price/self.old_price) * 100)
    #    return 0


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    alt_text = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)  # для порядка сортировки

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Фотография товара'
        verbose_name_plural = 'Фотографии товара'

    def __str__(self):
        return f"Фото для {self.product.name}"