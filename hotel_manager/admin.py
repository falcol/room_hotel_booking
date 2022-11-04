from django.contrib import admin

from .forms import HotelUpdateForm
from .models import HotelDetails

# Register your models here.


@admin.register(HotelDetails)
class HotelAdmin(admin.ModelAdmin):
    # form = HotelUpdateForm
    pass
