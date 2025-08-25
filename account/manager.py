from django.contrib.auth.models import BaseUserManager


class CustemUserManager(BaseUserManager):
    """
    Кастомный менеджер для модели User, обеспечивающий создание
    пользователей и суперпользователей с использованием email в качестве
    основного идентификатора вместо username.
    
    Наследует от BaseUserManager и переопределяет методы создания
    пользователей для работы с кастомной моделью User.
    """
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя с заданным email,
        username и паролем.
        
        Args:
            email (str): Email адрес пользователя (обязательный)
            username (str): Имя пользователя (обязательный)
            password (str, optional): Пароль пользователя. Может быть None.
            **extra_fields: Дополнительные поля модели пользователя.
        
        Returns:
            User: Созданный объект пользователя.
        
        Raises:
            ValueError: Если email или username не предоставлены.
        """
        if not email:
            raise ValueError("User must have an email address")
        elif not username:
            raise ValueError("User must have a username")
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            **extra_fields
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя с правами администратора.
        
        Автоматически устанавливает флаги is_staff, is_superuser и is_active
        в True для предоставления полных прав доступа.
        
        Args:
            email (str): Email адрес суперпользователя (обязательный)
            username (str): Имя суперпользователя (обязательный)
            password (str, optional): Пароль суперпользователя.
            **extra_fields: Дополнительные поля модели пользователя.
        
        Returns:
            User: Созданный объект суперпользователя.
        
        Raises:
            ValueError: Если флаги is_staff или is_superuser явно установлены в False.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)