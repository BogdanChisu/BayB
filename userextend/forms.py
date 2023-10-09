from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from userextend.models import BusinessUser


class BusinessUserForm(UserCreationForm):
    class Meta:
        model = BusinessUser
        fields = ('first_name', 'last_name', 'email', 'company')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'form-control',
                                                       'placeholder': 'Please enter your first name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control',
                                                      'placeholder': 'Please enter your last name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Please specify your e-mail address'})
        self.fields['company'].widget.attrs.update({'class': 'form-control',
                                                    'placeholder': 'Please specify company name'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control',
                                                      'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control',
                                                      'placeholder': 'Confirm password'})