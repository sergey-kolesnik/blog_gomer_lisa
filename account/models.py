from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .manager import CustemUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя, использующая email в качестве
    основного идентификатора для аутентификации вместо username.

    Наследует от:
        AbstractBaseUser: Базовая функциональность аутентификации
        PermissionsMixin: Система прав и разрешений Django

    Attributes:
        username (CharField): Уникальное имя пользователя.
        email (EmailField): Уникальный email адрес (используется для входа).
        is_staff (BooleanField): Определяет доступ к админ-панели.
        is_active (BooleanField): Определяет активность аккаунта.
        created (DateTimeField): Дата и время создания аккаунта.

    Meta:
        USERNAME_FIELD: Поле, используемое для аутентификации (email).
        REQUIRED_FIELDS: Обязательные поля при создании суперпользователя.
    """

    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    email = models.EmailField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Email address",
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustemUserManager()

    class Meta:
        indexes = [
            models.Index(fields=['email'], name='idx_email'),
            models.Index(fields=['username'], name='idx_username'),
        ]

    def __str__(self):
        return self.username
