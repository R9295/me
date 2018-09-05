from django import forms
from django.contrib.auth import forms as base_auth_forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from nocaptcha_recaptcha.fields import NoReCaptchaField

from me.base_forms import StyledForm

from .models import User


class UserCreationForm(StyledForm, BaseUserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
    captcha = NoReCaptchaField()
    field_css = {
        'email': 'uk-input',
        'password1': 'uk-input',
        'password2': 'uk-input',
    }

    field_icons = {
        'email': 'fas fa-envelope',
        'password1': 'fas fa-lock',
        'password2': 'fas fa-lock',
    }

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('email', )


class LoginForm(StyledForm, AuthenticationForm):
    field_css = {
        'username': 'uk-input',
        'password': 'uk-input',
    }
    field_icons = {
        'username': 'fas fa-envelope',
        'password': 'fas fa-lock',
    }


class SetPasswordForm(StyledForm, base_auth_forms.SetPasswordForm):

    field_css = {
        'new_password1': 'uk-input',
        'new_password2': 'uk-input',
    }
    field_icons = {
        'new_password1': 'lock',
        'new_password2': 'lock',
    }

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        # remove help text
        self.fields.get('new_password1').help_text = None


class PasswordResetForm(StyledForm, base_auth_forms.PasswordResetForm):
    field_css = {
        'email': 'uk-input',
    }
    field_icons = {
        'email': 'user',
    }


class SettingsForm(StyledForm, PasswordChangeForm):
    field_css = {
        'old_password': 'uk-input',
        'new_password1': 'uk-input',
        'new_password2': 'uk-input',
    }
    field_icons = {
        'old_password': 'fas fa-lock',
        'new_password1': 'fas fa-lock',
        'new_password2': 'fas fa-lock',
    }
    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields.get('new_password1').help_text = None
