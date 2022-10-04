from django.contrib import admin
from .models import HotelDetails
from .forms import HotelUpdateForm
# Register your models here.


@admin.register(HotelDetails)
class HotelAdmin(admin.ModelAdmin):
    form = HotelUpdateForm
    pass
