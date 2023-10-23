from django import forms
from django.forms import Select, TextInput, Textarea, CheckboxInput, \
    NumberInput, FileInput

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
            'image': FileInput(attrs={'class': 'form-control',
                                      'type': 'file'}),
            'price': NumberInput(attrs={'class': 'form-control',
                                        'placeholder': 'Please specify product price'}),
            'in_stock': CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        get_name = cleaned_data['model_name']

        check_models = Product.objects.filter(model_name=get_name)
        if check_models:
            msg = 'Product already exists!'
            self.errors['model_name'] = self.error_class([msg])

        return cleaned_data
