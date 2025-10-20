from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
import string


class CustomUser(AbstractUser):

    is_confirmed = models.BooleanField(
        default=False,
        verbose_name='Confirm'
    )

    def __str__(self):
        return self.username

class ActivationCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE ,related_name='activating_code')
    code = models.CharField(max_length=6)

    def generate_code(self):
        self.code = ''.join(secrets.choice(string.digits) for _ in range(6))
        self.save()
