from django import forms
from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation

from django.contrib.auth.validators import UnicodeUsernameValidator
username_validator = UnicodeUsernameValidator()


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username',
                  'password1', 'password2']

    first_name = forms.CharField(max_length=12, min_length=4, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'John'}))
    last_name = forms.CharField(max_length=12, min_length=4, required=True,
                                widget=(forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Doe'})))
    username = forms.CharField(
        label=_('Username'),
        max_length=150,
        help_text=_(
            '150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={'unique': _(
            "Username is already taken by another user.")},
        widget=forms.TextInput(
            attrs={'class': 'form__input', 'placeholder': 'john.doe'})
    )

    email = forms.EmailField(max_length=50, help_text='Required. Inform a valid email address.',
                             widget=(forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'john.doe@example.com'})))

    password1 = forms.CharField(label=_('Password'),
                                widget=(forms.PasswordInput(
                                    attrs={'class': 'form__input'})),
                                help_text=password_validation.password_validators_help_text_html())

    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput(attrs={'class': 'form__input'}),
                                help_text=_('Repeat the password for confirmation'))
