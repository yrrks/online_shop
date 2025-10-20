from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser
from .models import Wishlist



@receiver(post_save, sender=CustomUser)
def create_user_wishlist(sender, instance, created, **kwargs):
    if not created or instance.is_superuser:
        return

    try:
        # Создаем wishlist только для обычных пользователей
        Wishlist.objects.get_or_create(user=instance)
    except Exception as e:
        # Важно: НЕ поднимаем исключение, чтобы не сломать создание пользователя
        print(f"Notice: Не удалось создать wishlist для {instance.username}. Error: {e}")