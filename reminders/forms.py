from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import DateTimeInput

from .models import Reminder


class ReminderForm(forms.ModelForm):
    reminder = forms.DateTimeField(widget=DateTimeInput(attrs={
        "placeholder": "YYYY-MM-DD HH:MM:SS"
    }))

    class Meta:
        model = Reminder
        fields = ("subject", "message", "document", "reminder")


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["email", "password"]
