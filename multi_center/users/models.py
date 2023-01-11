from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import UsernameValidator

USER = 'user'
ADMIN = 'admin'
MANAGER = 'manager'


class User(AbstractUser):

    roles = (
        (USER, USER),
        (ADMIN, ADMIN),
        (MANAGER, MANAGER),
    )
    username_validator = UsernameValidator()
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
    first_name = models.CharField(
        'Имя',
        max_length=150, blank=True)
    last_name = models.CharField(
        'Фамилия',
        max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phone = models.CharField(
      verbose_name='Номер телефона', max_length=20,
      unique=True, null=True, blank=True)
    password = models.CharField(max_length=150)
    email = models.EmailField('Email', max_length=254, unique=True)
    role = models.CharField(
        'Роль пользователя',
        choices=roles,
        max_length=max(len(role[1]) for role in roles), default=USER
    )

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELDS = 'email'

    def __str__(self):
        return str(self.username)

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_manager(self):
        return self.role == MANAGER
