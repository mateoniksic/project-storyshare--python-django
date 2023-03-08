from .models import Tag
import re
from .models import Post
from django import forms
from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation

from django.contrib.auth.validators import UnicodeUsernameValidator
username_validator = UnicodeUsernameValidator()


class UserForm(UserCreationForm):
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


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['user_profile', 'slug',
                   'tags', 'date_created']

    title = forms.CharField(label='Title', max_length=148, required=True, widget=forms.TextInput(
        attrs={'class': 'form__input'}))

    content = forms.CharField(label='Content', max_length=64000, required=True, widget=forms.Textarea(
        attrs={'id': 'textarea', 'class': 'form__input', 'rows': 32, 'style': 'resize:none;'}))

    excerpt = forms.CharField(
        label='Excerpt', max_length=480, required=True, widget=forms.Textarea(
            attrs={'class': 'form__input', 'rows': 5, 'style': 'resize:none;'}))

    tag_list = forms.CharField(label='Tags', max_length=148, required=True, widget=forms.TextInput(
        attrs={'class': 'form__input'}))

    featured_image = forms.URLField(label='Featured image (URL)', widget=forms.URLInput(
        attrs={'class': 'form__input'}))
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.prefix = 'formPost'
        super(PostForm, self).__init__(*args, **kwargs)

    def clean_tag_list(self):
        tag_list = self.cleaned_data['tag_list'].split(' ')
        cleaned_tags = []

        for tag in tag_list:
            tag = tag.lower()
            tag = re.sub('[^a-zA-Z]+', '', tag)

            tag_exists = Tag.objects.filter(name=tag).exists()
            if tag_exists:
                tag = Tag.objects.filter(name=tag).get()
            else:
                tag = Tag(name=tag, slug=tag)
                tag.save()
            cleaned_tags.append(tag)

        return cleaned_tags

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        instance.user_profile = self.request.user.profile

        if commit:
            instance.save()

        tag_list = self.cleaned_data.get('tag_list')
        instance.tags.set(tag_list)

        return instance
