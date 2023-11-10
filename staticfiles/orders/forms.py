from django import forms
from django.forms import TextInput

from orders.models import PlaceOrder


class PlaceOrderForm(forms.ModelForm):
    class Meta:
        model = PlaceOrder
        fields = ['delivery_address']

        widgets = {
            'delivery_address': TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Please specify delivery address'})
        }

