from typing import Any, Dict

from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import BookingDetails, DrinkAndFood, RoomDetails, RoomPriceDetails


class RoomPriceDetailsForms(forms.ModelForm):

    class Meta:
        model = RoomPriceDetails
        fields = (
            'room_type',
            'price_per_day',
            'price_per_night',
            'price_first_two_hours',
            'price_next_hours',
            'max_person',
        )
        labels = {
            'room_type': 'Loại phòng',
            'hotel': "Khách sạn",
            'price_per_day': 'Giá một ngày (VNĐ)',
            'price_first_two_hours': 'Giá hai giờ đầu (VNĐ)',
            'price_next_hours': "Giá mỗi giờ tiếp theo (VNĐ)",
            'max_person': 'Số người tối đa',
            'price_per_night': 'Giá qua đêm'
        }

        widgets = {
            "room_type": forms.TextInput(attrs={
                "class": "form-control",
                "type": "text",
            }),
            "price_per_day": forms.TextInput(attrs={
                "class": "form-control",
                "type": "number",
            }),
            "price_per_night": forms.TextInput(attrs={
                "class": "form-control",
                "type": "number",
            }),
            "price_first_two_hours": forms.TextInput(attrs={
                "class": "form-control",
                "type": "number",
            }),
            "price_next_hours": forms.TextInput(attrs={
                "class": "form-control",
                "type": "number",
            }),
            "max_person": forms.TextInput(attrs={
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
    guest_phone_number = PhoneNumberField(region="VN")

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
        super(BookingDetailsForms, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.error_messages.update({'required': f'{field.label} không được bỏ trống'})


class RoomDetailsForms(forms.ModelForm):

    class Meta:
        model = RoomDetails
        fields = ('room_name', 'room_no', 'room_price', 'floor_no', 'size', 'room_status', 'layout', 'introduce')
        labels = {
            'booking': 'Đặt phòng',
            'room_name': 'Tên phòng',
            'room_no': 'Phòng số',
            'hotel': 'Thuộc khách sạn',
            'room_price': 'Giá phòng',
            'layout': 'Dịch vụ',
            'floor_no': 'Thuộc tầng',
            'size': 'Diện tích (m2)',
            'room_status': 'Trạng thái phòng',
            'introduce': 'Giới thiệu'
        }

        widgets = {
            "room_name": forms.TextInput(attrs={
                "class": "form-control",
                "type": "text",
            }),
            "room_no": forms.TextInput(attrs={
                "class": "form-control",
                "type": "number",
            }),
            "room_price": forms.Select(attrs={
                "class": "form-control",
            }),
            "layout": forms.Textarea(attrs={
                "class": "form-control",
            }),
            "introduce": forms.Textarea(attrs={
                "class": "form-control",
            }),
            "floor_no": forms.TextInput(attrs={
                "class": "form-control",
                "type": "number",
            }),
            "size": forms.TextInput(attrs={
                "class": "form-control",
                "type": "text",
            }),
            "room_status": forms.Select(attrs={
                "class": "form-control",
            }),
        }

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if self.is_valid():
            pass
        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.required = True
        super(RoomDetailsForms, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.error_messages.update({'required': f'{field.label} không được bỏ trống'})


class PhotoForms(forms.Form):
    images = forms.ImageField(
        label='Hình ảnh', required=True, widget=forms.FileInput(attrs={
            'class': 'form-control-file',
            'multiple': True
        }))

    def __init__(self, *args, **kwargs):
        self.required = True
        super(PhotoForms, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.error_messages.update({'required': f'{field.label}không được bỏ trống'})


class SearchRoomsEmty(forms.Form):

    datetime_check_in = forms.DateTimeField(
        label='Thời gian vào', widget=(forms.TextInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })))
    datetime_check_out = forms.DateTimeField(
        label='Thời gian ra', widget=(forms.TextInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })))
    max_person = forms.IntegerField(
        label='Số người ở', widget=(forms.TextInput(attrs={
            'type': 'number',
            'class': 'form-control'
        })))

    def clean(self):
        cleaned_data = super().clean()
        if self.is_valid():
            check_in = cleaned_data.get('datetime_check_in')
            check_out = cleaned_data.get('datetime_check_out')
            if check_in >= check_out:
                self.add_error('datetime_check_in', 'Thời gian vào không được lớn hơn thời gian ra')

    def __init__(self, *args, **kwargs):
        self.required = True
        super(SearchRoomsEmty, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.error_messages.update({'required': f'{field.label} không được bỏ trống'})


class BookingCheckOutForms(forms.ModelForm):
    guest_phone_number = PhoneNumberField(region="VN")

    class Meta:
        model = BookingDetails
        fields = (
            'guest_name',
            'guest_phone_number',
            'booking_type',
            'booking_status',
            'check_in_time',
            'check_out_time',
            'room',
            'total_guests',
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
            'booking_status': forms.Select(attrs={
                "class": "form-control",
            }),
            'total_cost': forms.TextInput(attrs={
                "class": "form-control",
                "type": "number",
            }),
            'discounted_price': forms.TextInput(attrs={
                "class": "form-control",
                "type": "number",
            }),
            'room': forms.TextInput(attrs={
                "class": "form-control",
                "type": "number",
            }),
        }

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if self.is_valid():
            pass

    def __init__(self, *args, **kwargs):
        self.required = True
        super(BookingCheckOutForms, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.error_messages.update({'required': f'{field.label} không được bỏ trống'})
