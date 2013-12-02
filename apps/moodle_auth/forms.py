import bcrypt

from django import forms
from django.core.exceptions import ValidationError

from registration.models import User


class MoodleForm(forms.Form):

    def clean(self):
        if(bcrypt.hashpw(self.cleaned_data.get('password'), salt) != salt):
            raise ValidationError("Incorrect Username or password")

        return self.cleaned_data

    username = forms.CharField(label='Moodle Username', required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def __init__(self, *args, **kwargs):

        if kwargs.get('instance'):
            username = kwargs['instance'].username
            # kwargs.setdefault('initial', {})['confirm_email'] = email

        return super(MoodleForm, self).__init__(*args, **kwargs)