from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.utils import get_user_role
from .models import Order, OrderStatus
from .forms import OrderCreateForm, OrderStatusForm, OrderAdminForm, OrderItemFormSet


@login_required
def order_list(request):
    """Список заказов с учётом роли"""
    role = get_user_role(request.user)

    if role == 'guest':
        messages.error(request, 'Для просмотра заказов необходимо войти в систему.')
        return redirect('products:product_list')

    if role in ('admin', 'manager'):
        orders = Order.objects.select_related('customer', 'status', 'pickup_point').all()
    else:
        orders = Order.objects.select_related('customer', 'status', 'pickup_point').filter(
            customer=request.user
        )

    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'user_role': role,
    })


@login_required
def order_create(request):
    """Создание заказа (клиент, администратор)"""
    role = get_user_role(request.user)

    if role not in ('client', 'admin'):
        messages.error(request, 'У вас нет прав для создания заказа.')
        return redirect('orders:order_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            # Устанавливаем начальный статус
            initial_status, _ = OrderStatus.objects.get_or_create(name='Новый')
            order.status = initial_status
            order.save()

            items = formset.save(commit=False)
            for item in items:
                item.order = order
                item.price = item.product.final_price
                item.save()
            for item in formset.deleted_objects:
                item.delete()

            messages.success(request, f'Заказ {order.order_number} успешно создан.')
            return redirect('orders:order_detail', pk=order.pk)
    else:
        form = OrderCreateForm()
        formset = OrderItemFormSet()

    return render(request, 'orders/order_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Создать заказ',
        'user_role': role,
    })


@login_required
def order_detail(request, pk):
    """Детальная страница заказа"""
    role = get_user_role(request.user)

    if role == 'guest':
        messages.error(request, 'Для просмотра заказа необходимо войти в систему.')
        return redirect('products:product_list')

    order = get_object_or_404(Order, pk=pk)

    # Клиент видит только свои заказы
    if role == 'client' and order.customer != request.user:
        messages.error(request, 'У вас нет доступа к этому заказу.')
        return redirect('orders:order_list')

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'user_role': role,
    })


@login_required
def order_update(request, pk):
    """Редактирование заказа (менеджер — только статус; администратор — полное)"""
    role = get_user_role(request.user)

    if role not in ('manager', 'admin'):
        messages.error(request, 'У вас нет прав для редактирования заказа.')
        return redirect('orders:order_list')

    order = get_object_or_404(Order, pk=pk)
    FormClass = OrderStatusForm if role == 'manager' else OrderAdminForm

    if request.method == 'POST':
        form = FormClass(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f'Заказ {order.order_number} успешно обновлён.')
            return redirect('orders:order_detail', pk=order.pk)
    else:
        form = FormClass(instance=order)

    return render(request, 'orders/order_form.html', {
        'form': form,
        'order': order,
        'title': 'Редактировать заказ',
        'user_role': role,
    })


@login_required
def order_delete(request, pk):
    """Удаление заказа (только администратор)"""
    role = get_user_role(request.user)

    if role != 'admin':
        messages.error(request, 'У вас нет прав для удаления заказа.')
        return redirect('orders:order_list')

    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        number = order.order_number
        order.delete()
        messages.success(request, f'Заказ {number} успешно удалён.')
        return redirect('orders:order_list')

    return render(request, 'orders/order_confirm_delete.html', {
        'order': order,
        'user_role': role,
    })
