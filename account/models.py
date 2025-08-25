from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin
    )
from django.utils import timezone

from .manager import CustemUserManager

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False
        )
    email = models.EmailField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Email address"
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        default=True
    )
    created = models.DateTimeField(
        default=timezone.now
        )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustemUserManager()
    
    def __str__(self):
        return self.username
