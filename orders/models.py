import uuid
from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class OrderStatus(models.Model):
    """Статус заказа"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Статус заказа"
        verbose_name_plural = "Статусы заказов"
        ordering = ['id']

    def __str__(self):
        return self.name


class PickupPoint(models.Model):
    """Пункт выдачи заказа"""
    address = models.CharField(max_length=300, unique=True, verbose_name="Адрес")

    class Meta:
        verbose_name = "Пункт выдачи"
        verbose_name_plural = "Пункты выдачи"
        ordering = ['address']

    def __str__(self):
        return self.address


class Order(models.Model):
    """Заказ"""
    order_number = models.CharField(max_length=50, unique=True, blank=True, verbose_name="Номер заказа")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    delivery_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата выдачи")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Покупатель")
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, verbose_name="Статус")
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.CASCADE, verbose_name="Пункт выдачи")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-order_date']

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def total(self):
        return sum(item.price * item.quantity for item in self.items.all())


class OrderItem(models.Model):
    """Позиция заказа"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена на момент заказа")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"
        unique_together = ('order', 'product')

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity
