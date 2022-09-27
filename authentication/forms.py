from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    username = forms.Field(
        label='Tên người dùng',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.Field(
        label='Mật khẩu',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.Field(
        label='Nhập lại mật khẩu',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    is_staff = forms.BooleanField(
        label='Bạn là chủ khách sạn?',
        widget=forms.CheckboxInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_staff']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.error_messages.update(
                {'required': f'{field.label} không được bỏ trống'})
