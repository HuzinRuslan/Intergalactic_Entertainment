from django.contrib.auth.models import AbstractUser
from django.db import models

from intergalactic.settings import USERS_AVATARS


class IntergalacticUser(AbstractUser):
    avatar = models.ImageField(upload_to=USERS_AVATARS, blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', null=False,
                                      default=0)
    email = models.EmailField(verbose_name='электронный адрес', unique=True)
    about = models.TextField(verbose_name='о себе', blank=True)
    company = models.CharField(verbose_name='компания', max_length=32,
                               blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-is_active', '-is_superuser', '-is_staff', 'username']
