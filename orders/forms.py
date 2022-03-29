from django import forms
from .models import OrderModel


class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'address_line_1',
                  'address_line_2', 'country', 'state', 'city', 'pincode', 'order_note')
