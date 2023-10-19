from django.forms import TextInput

from category.models import Category
from django import forms


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

        widgets = {
            'name': TextInput(attrs={'class': 'form-control',
                                              'placeholder':
                                                  'Specify category name'})
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        get_name = cleaned_data['name']

        check_categories = Category.objects.filter(name=get_name)
        if check_categories:
            msg = 'Category already exists!'
            self.errors['name'] = self.error_class([msg])

        return cleaned_data