from typing import Any, Dict
from django import forms
from .models import CustomerDetails


class CustomerDetailsForm(forms.ModelForm):

    class Meta:
        model = CustomerDetails
        fields = (
            'phone_number',
            'customer_id',
            'address',
            'city',
            'country',
        )
        labels = {
            "phone_number": "Số điện thoại",
            "address": "Địa chỉ",
            "city": "Thuộc thành phố",
            "country": "Quốc tịch"
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
