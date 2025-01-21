from django import forms
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ImageForm(forms.Form):
    image = forms.ImageField()
    
class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    phone_number = PhoneNumberField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username[0].isalpha():
            raise forms.ValidationError('Username must start with a letter.')
        return username

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError("Confirm Password must be the same as Password.")
        
        return confirm_password

    def create_user(self):
        # Manually create user and hash password
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        user = User.objects.create_user(username=username, email=email, password=password)
        return user
