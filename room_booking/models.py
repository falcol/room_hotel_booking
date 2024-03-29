from datetime import datetime

from django.db import models

from authentication.models import User
from hotel_manager.models import HotelDetails
from payment.models import Payment


class DrinkAndFood(models.Model):
    MENU_TYPE = (
        (0, "Đồ ăn"),
        (1, "Nước uống"),
    )
    hotel_id = models.ForeignKey(HotelDetails, on_delete=models.CASCADE, related_name="hotel_menu")
    menu_type = models.IntegerField(choices=MENU_TYPE, default=0)
    item_name = models.CharField(max_length=255, unique=True)
    total = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item_name


class RoomPriceDetails(models.Model):
    room_type = models.CharField(max_length=255)
    hotel = models.ForeignKey(
        HotelDetails, on_delete=models.CASCADE, related_name="rooms_hotel_prices", blank=True, null=True
    )
    price_per_day = models.PositiveIntegerField(default=0)
    price_first_two_hours = models.PositiveIntegerField(default=0)
    price_next_hours = models.PositiveIntegerField(default=0)
    price_per_night = models.PositiveIntegerField(default=0)
    max_person = models.PositiveIntegerField(default=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room_type


class RoomDetails(models.Model):
    ROOM_STATUS = (('E', 'Trống'), ('C', 'Đang dọn'), ('L', 'Cho thuê'))
    room_name = models.CharField(max_length=255)
    room_no = models.PositiveIntegerField(null=True)
    hotel = models.ForeignKey(HotelDetails, on_delete=models.CASCADE, related_name='room_hotel')
    room_price = models.ForeignKey(RoomPriceDetails, on_delete=models.CASCADE, blank=True, null=True)
    layout = models.TextField(blank=True)
    introduce = models.TextField(blank=True)
    rating_star = models.FloatField(blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, default="30")
    floor_no = models.PositiveIntegerField(default=0)
    room_status = models.CharField(choices=ROOM_STATUS, max_length=1, default="E")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room_name


class BookingDetails(models.Model):
    BOOKING_STATUS = (
        ('KH', 'Khách hàng hủy'), ('KSH', 'Khách sạn hủy'), ('TP', 'Trả phòng'), ('DP', 'Đặt phòng'),
        ("NP", "Nhận phòng")
    )
    booking_id = models.AutoField(primary_key=True)
    guest = models.ForeignKey(
        User, to_field='username', on_delete=models.CASCADE, null=True, related_name="guest_bookings"
    )
    guest_name = models.CharField(max_length=255, blank=True, null=True)
    guest_phone_number = models.CharField(max_length=255, blank=True, null=True)
    BOOKING_TYPE = ((0, "Nghỉ giờ"), (1, "Nghỉ qua đêm"), (2, "Nghỉ ngày"))
    booking_type = models.IntegerField(choices=BOOKING_TYPE, default=0)
    hotel = models.ForeignKey(HotelDetails, on_delete=models.CASCADE, related_name="hotel_bookings")
    booking_status = models.CharField(max_length=3, choices=BOOKING_STATUS, default='DP')
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    room = models.ForeignKey(RoomDetails, on_delete=models.CASCADE, related_name="room_bookings")
    total_guests = models.PositiveIntegerField(default=0)
    total_cost = models.FloatField(default=0)
    discounted_price = models.FloatField(default=0)
    booking_date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    pre_order = models.BooleanField(default=False)
    is_pay = models.BooleanField(default=False)
    pay_online = models.OneToOneField(
        Payment, on_delete=models.DO_NOTHING, related_name="pay_online", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.guest_name


class DrinkAndFoodOrder(models.Model):
    drink_and_food = models.ForeignKey(DrinkAndFood, related_name="food", on_delete=models.DO_NOTHING)
    book = models.ForeignKey(BookingDetails, related_name="menu", on_delete=models.DO_NOTHING, default=None)
    total = models.IntegerField(default=0)
    amount = models.FloatField(default=0)
    accept = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.drink_and_food)


class Photos(models.Model):
    hotel_id = models.ForeignKey(
        HotelDetails, on_delete=models.CASCADE, related_name='hotel_photos', blank=True, null=True
    )
    room_id = models.ForeignKey(
        RoomDetails, on_delete=models.CASCADE, blank=True, null=True, related_name='room_photos'
    )
    FOLDER_NAME = datetime.strftime(datetime.now(), "%Y%m%d")
    image_hotel = models.ImageField(upload_to=f'hotels/{FOLDER_NAME}/', blank=True, null=True)
    image_room = models.ImageField(upload_to=f'rooms/{FOLDER_NAME}/', blank=True, null=True)
    image_name = models.CharField(max_length=255, default="image")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image_name
