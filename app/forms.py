from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Image, Profile, Comments


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class SigninForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    password = forms.PasswordInput()

class ImageForm(forms.ModelForm):
    
    class Meta:
        model = Image
        exclude = ['likes', 'post_date', 'Profile']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['image', 'user']