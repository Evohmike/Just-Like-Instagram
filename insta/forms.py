from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']



class ImageForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user']