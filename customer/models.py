from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from authentication.models import User
from hotel_manager.models import HotelDetails
from room_booking.models import RoomDetails


class CustomerDetails(models.Model):
    phone_number = PhoneNumberField(blank=True, max_length=255, region="VN")
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="info")
    address = models.CharField(blank=True, max_length=255)
    city = models.CharField(blank=True, max_length=255)
    country = models.CharField(blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.phone_number)


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    hotel = models.ForeignKey(HotelDetails, on_delete=models.CASCADE, related_name="comments")
    room = models.ForeignKey(RoomDetails, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.comment


class RatingStars(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rating")
    hotel = models.ForeignKey(HotelDetails, on_delete=models.CASCADE, related_name="rating")
    room = models.ForeignKey(RoomDetails, on_delete=models.CASCADE, related_name="rating")
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.rating)
