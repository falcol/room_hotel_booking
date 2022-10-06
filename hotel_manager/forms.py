from typing import Any, Dict
from django import forms
from .models import HotelDetails


class HotelCreateForm(forms.ModelForm):

    class Meta:
        model = HotelDetails
        fields = ('name', 'email', 'contact_no', 'address', 'city', 'introduce')
        labels = {
            "name": "Tên khách sạn",
            "email": "Email khách sạn",
            "contact_no": "Số điện thoại",
            "address": "Địa chỉ khách sạn",
            "city": "Thuộc thành phố",
            "introduce": "Dịch vụ"
        }

        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if self.is_valid():
            pass
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(HotelCreateForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.error_messages.update({'required': f'{field.label}không được bỏ trống'})


class HotelUpdateForm(forms.ModelForm):

    class Meta:
        model = HotelDetails
        fields = ('name', 'email', 'contact_no', 'owner', 'address', 'city', 'latitude', 'logtitude', 'introduce')
        labels = {
            "name": "Tên khách sạn",
            "email": "Email khách sạn",
            "contact_no": "Số điện thoại",
            "address": "Địa chỉ khách sạn",
            "city": "Thuộc thành phố",
            "latitude": "Vĩ độ",
            "logtitude": "Kinh độ",
            "introduce": "Dịch vụ"
        }

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if self.is_valid():
            pass
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(HotelUpdateForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.error_messages.update({'required': f'{field.label}không được bỏ trống'})
