from django.contrib.auth.models import AbstractUser
from django.db import models

from mailing.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='users/', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    is_verified = models.BooleanField(default=False, verbose_name='почта верифицирована')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
