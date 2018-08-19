from django import forms
from django.core.exceptions import ValidationError

from .models import Profile


class ProfileForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        if 'user' in self.changed_data and self.cleaned_data.get('user'):
            if self.initial['user'] != str(self.cleaned_data.get('user').pk):
                raise ValidationError({'user': "The user you're trying to edit is not you!"})
        return cleaned_data

    class Meta:
        model = Profile
        fields = ('user', 'prefix', 'first_name', 'last_name', 'short_description',
                  'description', 'github', 'facebook',
                  'medium', 'twitter', 'linkedin', 'theme',)
        widgets = {
            'user': forms.HiddenInput()
        }
