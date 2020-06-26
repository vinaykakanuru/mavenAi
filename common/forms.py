from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class SignUpForm(UserCreationForm):
    """ SignUpForm for User Creation """
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(
        max_length=254, required=True, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2',]

    # check if username exists
    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("Username already Taken")

    # check if Email exists
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email addresses must be unique.')
        return email


class UserForm(forms.ModelForm):
    """ UserForm for Profile Updation Form """
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(
        max_length=254, required=True, help_text='Enter a valid email address')
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    # check if Email exists
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email addresses must be unique.')
        return email

class ProfileForm(forms.ModelForm):
    """ ProfileForm for Profile Updation Form """
    class Meta:
        model = Profile
        fields = [
            'full_name', 'phone_number', 'passport_number', 'birth_date', 'age', 'profile_image',
        ]

    # Check the Age and save only if greater than 16
    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 16:
            raise forms.ValidationError('User should be greater than 16 years')
        return age

class FormLogin(forms.Form):
    """ For Login Form """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
