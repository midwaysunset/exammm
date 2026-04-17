from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem, OrderStatus, PickupPoint


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['pickup_point']
        widgets = {
            'pickup_point': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'pickup_point': 'Пункт выдачи',
        }


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'status': 'Статус',
        }


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'pickup_point', 'delivery_date']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'pickup_point': forms.Select(attrs={'class': 'form-select'}),
            'delivery_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
        }
        labels = {
            'status': 'Статус',
            'pickup_point': 'Пункт выдачи',
            'delivery_date': 'Дата выдачи',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.delivery_date:
            self.fields['delivery_date'].initial = (
                self.instance.delivery_date.strftime('%Y-%m-%dT%H:%M')
            )


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }
        labels = {
            'product': 'Товар',
            'quantity': 'Количество',
        }


OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    fields=['product', 'quantity'],
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)
