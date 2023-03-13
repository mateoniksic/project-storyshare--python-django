from django import forms
from django.forms import ModelForm
from .models import *

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User

from django.utils.text import slugify
import re


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username',
                  'password1', 'password2']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Doe'}),
            'username': forms.TextInput(
                attrs={'class': 'form__input', 'placeholder': 'john.doe'}),
            'email': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'john.doe@example.com'}),

        }

    password1 = forms.CharField(label='New password', required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form__input'}))
    password2 = forms.CharField(label='Confirm password', required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form__input'}))

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.prefix = 'CustomUserCreationForm'


class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = 'CustomAuthenticationForm'
        self.fields['username'].widget = forms.TextInput(
            attrs={'class': 'form__input'})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': 'form__input'})


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form__input', 'placeholder': 'john.doe'}),
            'first_name': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Doe'}),
            'email': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'john.doe@example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = 'user_update_form'



class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'description']

        labels = {
            'profile_image': 'Profile image (URL)',
            'description': 'Profile description'
        }

        widgets = {
            'profile_image': forms.URLInput(
                attrs={'class': 'form__input', 'placeholder': 'https://www.example.com/my-profile-image'}),
            'description': forms.Textarea(
                attrs={'class': 'form__input', 'rows': 4, 'style': 'resize:none;', 'placeholder': 'Describe yourself shortly.'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = 'UserProfileForm'


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'featured_image']

        labels = {
            'title': 'Story title',
            'content': 'Story content',
            'excerpt': 'Story summary',
            'featured_image': 'Featured image (URL)'
        }

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form__input', 'placeholder': 'Enter your attention grabbing title'}),
            'content': forms.Textarea(
                attrs={'id': 'textarea', 'class': 'form__input', 'rows': 32, 'style': 'resize:none;', 'placeholder': 'Enter high value content'}),
            'excerpt': forms.Textarea(
                attrs={'class': 'form__input', 'rows': 5, 'style': 'resize:none;', 'placeholder': 'Enter short summary of your high value content'}),
            'featured_image': forms.URLInput(
                attrs={'class': 'form__input', 'placeholder': 'https://www.example.com/my-featured-image'})
        }

        required = {
            'title': True,
            'content': True,
            'excerpt': True,
            'featured_image': True
        }

    tag_list = forms.CharField(label='Tags', max_length=148, required=True, widget=forms.TextInput(
        attrs={'class': 'form__input', 'placeholder': 'mytag1 mytag2'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.prefix = 'PostForm'
        super(PostForm, self).__init__(*args, **kwargs)

    def clean_tag_list(self):
        tag_list = self.cleaned_data['tag_list'].split(' ')
        cleaned_tag_list = []

        for tag in tag_list:
            tag = slugify(re.sub('[^a-zA-Z0-9]+', '', tag))

            if tag:
                tag, created = Tag.objects.get_or_create(name=tag, slug=tag)
                cleaned_tag_list.append(tag)

        return cleaned_tag_list

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)

        instance.user_profile = self.request.user.profile

        if commit:
            instance.save()

        cleaned_tag_list = self.cleaned_data.get('tag_list')
        instance.tags.set(cleaned_tag_list)

        return instance
