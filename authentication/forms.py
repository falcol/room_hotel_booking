from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    username = forms.Field(
        label='Ten tai khoan',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.Field(
        label='Mat khau',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.Field(
        label='Nhap lai mat khau',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
