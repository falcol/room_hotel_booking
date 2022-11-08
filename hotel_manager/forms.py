from typing import Any, Dict

from django import forms
from phonenumber_field.formfields import PhoneNumberField

from room_booking.models import BookingDetails, DrinkAndFood, Photos

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

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "type": "text",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "type": "text",
            }),
            "contact_no": forms.TextInput(attrs={
                "class": "form-control",
                "type": "text",
            }),
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "type": "text",
            }),
            "city": forms.TextInput(attrs={
                "class": "form-control",
                "type": "text",
            }),
            "introduce": forms.Textarea(attrs={
                "class": "form-control",
            }),
        }

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if self.is_valid():
            pass
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(HotelCreateForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.required = True
            field.error_messages.update({'required': f'{field.label} không được bỏ trống'})


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
            field.error_messages.update({'required': f'{field.label} không được bỏ trống'})


class HotelBookUpdate(forms.ModelForm):
    guest_phone_number = PhoneNumberField(label="Số điện thoại", region="VN")

    class Meta:
        model = BookingDetails
        fields = (
            'guest_name',
            'guest_phone_number',
            'booking_type',
            'check_in_time',
            'check_out_time',
            'total_guests',
        )
        labels = {
            'guest': 'Khách hàng',
            'guest_name': 'Tên khách hàng',
            'guest_phone_number': 'Số điện thoại',
            'booking_type': 'Nghỉ loại',
            'hotel': 'Khách sạn',
            'booking_status': 'Trạng thái',
            'check_in_time': 'Thời gian nhận phòng',
            'check_out_time': 'Thời gian trả phòng',
            'room': 'Phòng',
            'total_guests': 'Số người',
            'drink_and_food': 'Menu',
            'total_cost': 'Tổng tiền',
            'discounted_price': 'Giảm giá',
        }

        widgets = {
            "guest_name": forms.TextInput(attrs={
                "class": "form-control",
                "type": "text",
            }),
            "booking_type": forms.Select(attrs={
                "class": "form-control",
            }),
            "check_in_time": forms.TextInput(attrs={
                "class": "form-control",
                "type": "datetime-local",
            }),
            "check_out_time": forms.TextInput(attrs={
                "class": "form-control",
                "type": "datetime-local",
            }),
            "total_guests": forms.TextInput(attrs={
                "class": "form-control",
                "type": "number",
            }),
        }

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if self.is_valid():
            pass
        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.required = True
        super(HotelBookUpdate, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.error_messages.update({'required': f'{field.label} không được bỏ trống'})


class UpdatePhotoHotel(forms.ModelForm):

    class Meta:
        model = Photos
        fields = ['image_hotel']


class CreateUpdateMenu(forms.ModelForm):

    class Meta:
        model = DrinkAndFood
        fields = ('menu_type', 'item_name', 'price', 'total')

        labels = {
            'menu_type': 'Loại',
            'item_name': 'Tên đồ ăn/nước uống',
            'total': 'Số lượng',
            'price': 'Giá tiền(Nghìn VNĐ)',
        }
