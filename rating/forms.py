from django import forms
from django.forms import Select, Textarea

from rating.models import Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = '__all__'

        widgets = {
            'rating_val': Select(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control',
                                           'placeholder': 'Please share your experience'})
        }