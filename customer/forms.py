from typing import Any, Dict

from django import forms
from phonenumber_field.formfields import PhoneNumberField

from authentication.models import User

from .models import CustomerDetails


class CustomerDetailsForm(forms.ModelForm):
    phone_number = PhoneNumberField(label="Số điện thoại", region="VN")

    class Meta:
        model = CustomerDetails
        fields = (
            'phone_number',
            'city',
            'country',
        )
        labels = {
            "phone_number": "Số điện thoại",
            "address": "Địa chỉ",
            "city": "Hiện tại đang ở thành phố",
            "country": "Quốc gia"
        }

        widgets = {
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "type": "text",
            }),
            "city": forms.TextInput(attrs={
                "class": "form-control",
                "type": "text",
            }),
            "country": forms.TextInput(attrs={
                "class": "form-control",
                "type": "text",
            }),
        }

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if self.is_valid():
            pass
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(CustomerDetailsForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.error_messages.update({'required': f'{field.label}không được bỏ trống'})


class UserInfoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'email',
            'name',
        )
        labels = {
            "email": "Email",
            "name": "Tên người dùng",
        }

        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "type": "text",
            }),
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "type": "text",
            }),
        }

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if self.is_valid():
            pass
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.error_messages.update({'required': f'{field.label}không được bỏ trống'})
