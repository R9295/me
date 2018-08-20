from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from .models import User

FIELD_CLASSES = {
    'email': 'uk-input',
    'password1': 'uk-input',
    'password2': 'uk-input',
}

FIELD_ICONS = {
    'email': 'user',
    'password1': 'lock',
    'password2': 'lock',
}
class UserCreationForm(BaseUserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        # set classes
        for k, v in self.fields.items():
            v.widget.attrs['class'] = FIELD_CLASSES.get(k)
            v.widget.icon = FIELD_ICONS.get(k)

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
