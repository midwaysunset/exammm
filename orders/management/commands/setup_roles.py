"""
Команда для создания начальных данных:
  - группы пользователей (Клиенты, Менеджеры)
  - статусы заказов
  - пункты выдачи

Использование:
    python manage.py setup_roles
"""
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from orders.models import OrderStatus, PickupPoint


class Command(BaseCommand):
    help = 'Создаёт группы пользователей, статусы заказов и пункты выдачи'

    def handle(self, *args, **options):
        # Группы
        for group_name in ('Клиенты', 'Менеджеры'):
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создана группа: {group_name}'))
            else:
                self.stdout.write(f'Группа уже существует: {group_name}')

        # Статусы заказов
        statuses = ['Новый', 'В обработке', 'Готов к выдаче', 'Выдан', 'Отменён']
        for name in statuses:
            status, created = OrderStatus.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создан статус: {name}'))
            else:
                self.stdout.write(f'Статус уже существует: {name}')

        # Пункты выдачи
        points = [
            'ул. Ленина, 1',
            'пр. Мира, 45',
            'ул. Садовая, 12',
        ]
        for address in points:
            point, created = PickupPoint.objects.get_or_create(address=address)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создан пункт выдачи: {address}'))
            else:
                self.stdout.write(f'Пункт выдачи уже существует: {address}')

        self.stdout.write(self.style.SUCCESS('\nНастройка завершена.'))
