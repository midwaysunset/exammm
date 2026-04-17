from django.contrib import admin
from .models import OrderStatus, PickupPoint, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'status', 'pickup_point', 'order_date')
    list_filter = ('status',)
    inlines = [OrderItemInline]


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    ...


@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    ...


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    ...
