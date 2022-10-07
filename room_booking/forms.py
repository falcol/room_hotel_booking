from typing import Any, Dict
from django import forms
from django.forms import ModelChoiceField

from hotel_manager.models import HotelDetails
from .models import RoomPriceDetails, DrinkAndFood, BookingDetails, RoomDetails


class RoomPriceDetailsForms(forms.ModelForm):

    class Meta:
        model = RoomPriceDetails
        fields = (
            'room_type',
            'hotel',
            'price_per_day',
            'price_first_two_hours',
            'price_next_hours',
            'max_person',
        )
        labels = {
            'room_type': 'Loại phòng',
            'hotel': "Khách sạn",
            'price_per_day': 'Giá một ngày',
            'price_first_two_hours': 'Giá hai giờ đầu',
            'price_next_hours': "Giá mỗi giờ tiếp theo",
            'max_person': 'Số người tối đa',
        }

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if self.is_valid():
            pass
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(RoomPriceDetailsForms, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.error_messages.update({'required': f'{field.label}không được bỏ trống'})


class DrinkAndFoodForms(forms.ModelForm):

    class Meta:
        model = DrinkAndFood
        fields = (
            'hotel_id',
            'item_name',
            'price',
        )
        labels = {
            'hotel_id': 'Khách sạn',
            'item_name': 'Tên',
            'price': 'Giá',
        }

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if self.is_valid():
            pass
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(DrinkAndFoodForms, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.error_messages.update({'required': f'{field.label}không được bỏ trống'})


class BookingDetailsForms(forms.ModelForm):

    class Meta:
        model = BookingDetails
        fields = (
            'guest',
            'guest_name',
            'guest_phone_number',
            'booking_type',
            'hotel',
            'booking_status',
            'check_in_time',
            'check_out_time',
            'room',
            'total_guests',
            'drink_and_food',
            'total_cost',
            'discounted_price',
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
            'total_guests': 'Tổng khách',
            'drink_and_food': 'Menu',
            'total_cost': 'Tổng tiền',
            'discounted_price': 'Giảm giá',
        }

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if self.is_valid():
            pass
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(BookingDetailsForms, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.error_messages.update({'required': f'{field.label}không được bỏ trống'})


class RoomDetailsForms(forms.ModelForm):

    class Meta:
        model = RoomDetails
        fields = (
            'room_name',
            'room_no',
            'room_price',
            'layout',
            'floor_no',
            'room_status',
        )
        labels = {
            'booking': 'Đặt phòng',
            'room_name': 'Tên phòng',
            'room_no': 'Phòng số',
            'hotel': 'Thuộc khách sạn',
            'room_price': 'Giá phòng',
            'layout': 'Giới thiệu',
            'floor_no': 'Thuộc tầng',
            'room_status': 'Trạng thái phòng',
        }

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if self.is_valid():
            pass
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(RoomDetailsForms, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.error_messages.update({'required': f'{field.label}không được bỏ trống'})


class PhotoForms(forms.Form):
    images = forms.ImageField(label='Hình ảnh',
                              required=True,
                              widget=forms.FileInput(attrs={
                                  'class': 'form-control-file',
                                  'multiple': True
                              }))

    def __init__(self, *args, **kwargs):
        self.required = True
        super(PhotoForms, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.error_messages.update({'required': f'{field.label}không được bỏ trống'})
