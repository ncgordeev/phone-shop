from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from utils.utils import NULLABLE


class CustomUser(AbstractUser):
    """Кастомная модель пользователя"""

    class UserRolesChoices(models.TextChoices):
        USER = 'user', _('Пользователь')
        ADMIN = 'admin', _('Администратор')

    username = None
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    phone = models.CharField(max_length=15, verbose_name='Номер телефона')
    email = models.EmailField(unique=True, max_length=30, verbose_name='Email')
    avatar = models.ImageField(upload_to='users/', default='users/no_avatar.png', verbose_name='Аватар', **NULLABLE)
    role = models.CharField(max_length=10, choices=UserRolesChoices, default=UserRolesChoices.USER, verbose_name='Роль')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}, {self.role}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
