from django import forms
from django.core.exceptions import ValidationError
from .models import User

class SignupForm(forms.Form):
    full_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "")
        return cleaned_data


class LoginForm(forms.Form):
    email_or_phone = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)