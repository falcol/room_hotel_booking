from django.contrib import admin
from .models import HotelDetails
# Register your models here.


@admin.register(HotelDetails)
class HotelAdmin(admin.ModelAdmin):
    pass
