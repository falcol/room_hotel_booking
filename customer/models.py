from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from authentication.models import User


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
