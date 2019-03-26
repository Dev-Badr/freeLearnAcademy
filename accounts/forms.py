from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import widgets
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(
            attrs={'placeholder': "Email or Username", "class": "form-control"})
        self.fields['password'].widget = widgets.PasswordInput(
            attrs={'placeholder': "password", "class": "form-control"})


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = widgets.TextInput(
            attrs={'placeholder': "username", "class": "form-control"})
        self.fields['email'].widget = widgets.EmailInput(
            attrs={'placeholder': "email", "class": "form-control"})
        self.fields['password1'].widget = widgets.PasswordInput(
            attrs={'placeholder': "password", "class": "form-control"})
        self.fields['password2'].widget = widgets.PasswordInput(
            attrs={'placeholder': "repeat password", "class": "form-control"})

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',)

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo', 'gender', 'bio', 'mobile',
                    'prev_languages', 'twitter', 'facebook', 'github')