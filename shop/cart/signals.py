from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from accounts.models import CustomUser
from .models import Cart
from .cart import CartService

@receiver(post_save, sender=CustomUser)
def create_user_cart(sender, instance, created, **kwargs):
    if instance.is_staff or instance.is_superuser:
        return
    if created:
        try:
            # Создаем cart только для обычных пользователей
            Cart.objects.get_or_create(user=instance)
        except Exception as e:
            # Важно: НЕ поднимаем исключение, чтобы не сломать создание пользователя
            print(f"Notice: Не удалось создать cart для {instance.username}. Error: {e}")

@receiver(user_logged_in)
def load_user_cart(sender, request, user, **kwargs):
    """Загружаем корзину пользователя после логина"""
    cart = CartService(request)
    cart._load_from_db()