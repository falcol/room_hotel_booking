from django.db import models
from django.contrib.auth.models import AbstractUser
from customer.models import CustomerDetails
from room_booking.models import HotelDetails


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    guest = models.OneToOneField(CustomerDetails,
                                 null=True,
                                 blank=True,
                                 on_delete=models.CASCADE)
    hotel = models.ManyToManyField(HotelDetails,
                                   on_delete=models.CASCADE,
                                   blank=True,
                                   null=True)

    def __str__(self):
        return self.email
