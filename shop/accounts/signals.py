from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser
from .models import ActivationCode
from .tasks import get_confirm_code


@receiver(post_save, sender=CustomUser)
def create_activation_code(sender, instance, created, **kwargs):
    if (instance.is_superuser or instance.is_staff) and instance.is_confirmed == False:
        CustomUser.objects.filter(id=instance.id).update(is_confirmed=True)
        return
    if created and (not instance.is_superuser and not instance.is_staff):
        try:
            # Создаем code только для обычных пользователей
            code,_ = ActivationCode.objects.get_or_create(user=instance)
            code.generate_code()

            get_confirm_code.delay(instance.id)
        except Exception as e:
            # Важно: НЕ поднимаем исключение, чтобы не сломать создание пользователя
            print(f"Notice: Не удалось создать code для {instance.username}. Error: {e}")