from django import forms
from django.forms import widgets

class HomeRegisterForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32,
        widget = widgets.TextInput(
            attrs={'placeholder': "username", "class": "form-control"})
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 64,
        widget = widgets.EmailInput(
            attrs={'placeholder': "email", "class": "form-control"})
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = widgets.PasswordInput(
            attrs={'placeholder': "password", "class": "form-control"})
    )