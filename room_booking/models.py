from django.db import models
from authentication.models import User


class HotelDetails(models.Model):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True, unique=True)
    reg_no = models.CharField(max_length=255, blank=True)
    contact_no = models.CharField(max_length=255, blank=True)
    owner_name = models.CharField(max_length=255, blank=True)
    owner_email = models.EmailField(max_length=255, blank=True, unique=True)
    owner_contact_no = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=400, blank=True, unique=True)
    city = models.CharField(max_length=255, blank=True)
    imgages = models.ImageField(upload_to='hotels/')

    def __str__(self):
        return self.name


class RoomPriceDetails(models.Model):
    room_type = models.CharField(max_length=255, primary_key=True)
    hotel = models.ForeignKey(HotelDetails, to_field='hotel_id')
    price_per_day = models.PositiveIntegerField(default=0)
    price_first_two_hours = models.PositiveIntegerField(default=0)
    price_next_hours = models.PositiveIntegerField(default=0)


class DrinkAndFood(models.Model):
    name = models.CharField(max_length=255, blank=True)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name + ' ' + self.price


class BookingDetails(models.Model):
    BOOKING_STATUS = (('C', 'Còn phòng'), ('D', 'Đã có người đặt'),
                      ('KH', 'Khách hàng hủy'), ('KSH', 'Khách sạn hủy'))
    booking_id = models.AutoField(primary_key=True)
    guest = models.ForeignKey(User,
                              to_field='username',
                              on_delete=models.CASCADE)
    hotel = models.ForeignKey(HotelDetails, on_delete=models.CASCADE)
    booking_status = models.CharField(max_length=3, choices=BOOKING_STATUS)
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField()
    room = models.ForeignKey(RoomPriceDetails, to_field='room_type')
    total_guests = models.PositiveIntegerField(default=0)
    drink_and_food = models.ManyToManyField(DrinkAndFood,
                                            related_name='name',
                                            on_deleted=models.CASCADE())
    total_cost = models.FloatField()
    discounted_price = models.FloatField()
    total_rooms = models.PositiveIntegerField(default=0)
    booking_date = models.CharField(max_length=15)


class RoomDetails(models.Model):
    ROOM_STATUS = (('T', 'Trống'), ('B', 'Bẩn'), ('C', 'Cho thuê'), ('D',
                                                                     'Đã đặt'))
    booking = models.ForeignKey(BookingDetails,
                                to_field='booking_id',
                                null=True)
    room_key = models.AutoField(primary_key=True)
    room_no = models.PositiveIntegerField(null=True)
    hotel = models.ForeignKey(HotelDetails, to_field='hotel_id')
    guest = models.ForeignKey(User, to_field='username')
    room_price = models.ForeignKey(RoomPriceDetails, to_field='room_type')
    layout = models.CharField(max_length=40)
    floor_no = models.PositiveIntegerField(default=0)
    room_status = models.CharField(max_length=1)
    image = models.ImageField(upload_to='rooms/')
