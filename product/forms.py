from django import forms
from django.forms import Select, TextInput, Textarea, CheckboxInput

from product.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        widgets = {
            'category': Select(attrs={'class': 'form-select'}),
            'title': TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Enter product title'}),
            'manufacturer': TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Specify manufacturer'}),
            'model_name': TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Specify model'}),
            'description': Textarea(attrs={'class': 'form-control',
                                           'placeholder': 'Enter a brief product description'}),
            'in_stock': CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': CheckboxInput(attrs={'class': 'form-check-input'})
        }
