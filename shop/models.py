import os

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image

from users.models import CustomUser
from utils.utils import NULLABLE


def validate_image(image):
    valid_extensions = ['jpg', 'jpeg', 'png', 'webp']
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(_(f'Unsupported file type {ext}. Supported types: {", ".join(valid_extensions)}'))


class Category(models.Model):
    """Категории товаров"""

    title = models.CharField(max_length=255, verbose_name='Название категории')
    description = models.TextField(verbose_name='Описание категории')
    image = models.ImageField(upload_to='categories/', verbose_name='Изображение категории')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Product(models.Model):
    """Товары"""

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    title = models.CharField(max_length=255, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание товара', **NULLABLE)
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена товара')
    quantity = models.PositiveIntegerField(verbose_name='Количество товара')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def clean(self):
        super().clean()
        if self.price <= 0:
            raise ValidationError(_('Price must be positive.'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['title']


class ProductImage(models.Model):
    """Изображения товаров"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    image = models.ImageField(upload_to='products/', validators=[validate_image], verbose_name='Изображение товара')
    description = models.CharField(max_length=255, **NULLABLE, verbose_name='Описание')
    is_main = models.BooleanField(default=False, verbose_name='Основное изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def clean(self):
        super().clean()
        if self.image:
            img = Image.open(self.image)
            if img.file.size > (2 * 1024 * 1024):
                raise ValidationError(_('Image size must be less than 2 MB.'))

    def __str__(self):
        return f'{self.product.title}, {self.image}'

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
        indexes = [
            models.Index(fields=['product']),
        ]


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        NEW = 'new', _('Новый')
        IN_PROGRESS = 'in_progress', _('В процессе')
        PROCESSED = 'processed', _('Обработан')
        COMPLETED = 'completed', _('Завершен')
        CANCELED = 'canceled', _('Отменен')
        EXPIRED = 'expired', _('Истек срок действия')

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders',
                             verbose_name='Пользователь')
    product = models.ManyToManyField(Product, related_name='orders', verbose_name='Товар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=30, choices=OrderStatus, default=OrderStatus.NEW,
                              verbose_name='Статус заказа')

    def __str__(self):
        products_list = ', '.join(str(product) for product in self.product.all())
        return f'{self.user.email}, {products_list}, {self.created_at}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='carts', verbose_name='Корзина')
    product = models.ManyToManyField(Product, related_name='carts', verbose_name='Товар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        products_list = ', '.join(str(product) for product in self.product.all())
        return f'{products_list}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
