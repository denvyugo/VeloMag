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


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = (
        (MALE, 'M'),
        (FEMALE, 'F'),
    )

    user = models.OneToOneField(ShopUser, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='tags', max_length=128, blank=True)
    aboutMe = models.TextField(verbose_name='about me', max_length=512, blank=True)
    gender = models.CharField(verbose_name='gender', max_length=1, choices=GENDER_CHOICES, blank=True)
