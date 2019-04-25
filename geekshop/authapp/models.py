from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


def activation_key_expires():
    return now() + timedelta(hours=48)


# Create your models here.
class ShopUser(AbstractUser):

    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=activation_key_expires)

    def is_activation_key_expired(self):
        return now() > self.activation_key_expires
