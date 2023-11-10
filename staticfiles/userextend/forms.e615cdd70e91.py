from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, \
    PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'form-control',
                                                       'placeholder': 'Please enter your first name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control',
                                                      'placeholder': 'Please enter your last name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Please specify your e-mail address'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control',
                                                      'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control',
                                                      'placeholder': 'Confirm password'})

class UserBusinessForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'form-control',
                                                       'placeholder': 'Please enter your company name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control',
                                                      'placeholder': 'Please enter your last name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Please specify your e-mail address'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control',
                                                      'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control',
                                                      'placeholder': 'Confirm password'})




class AuthenticationNewForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control',
                                                     'placeholder': 'Please type your username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control',
                                                     'placeholder': 'Please type your password'})


class PasswordChangeNewForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs.update({'class': 'form-control',
                                                         'placeholder': 'Type your current password'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control',
                                                          'placeholder': 'Define your new password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control',
                                                          'placeholder': 'Confirm you new password'})
class PasswordResetNewForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'form-control',
                                                  'placehodler': 'Specify your email address'})

class SetPasswordNewForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.fields['new_password1'].widget.attrs.update({'class': 'form-control',
                                                          'placeholder': 'Specify your new password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control',
                                                           'placeholder': 'Confirm your new password'})
