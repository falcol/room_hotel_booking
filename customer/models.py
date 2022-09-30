from django.db import models


class CustomerDetails(models.Model):
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=400)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
