from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from authentication.models import User


class HotelDetails(models.Model):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True, unique=True)
    contact_no = PhoneNumberField(max_length=255, blank=True, region="VN")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hotels")
    address = models.CharField(max_length=400, blank=True, unique=True)
    city = models.CharField(max_length=255, blank=True)
    introduce = models.TextField(blank=True)
    latitude = models.CharField(blank=True, max_length=255)
    logtitude = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.name
