from django.contrib import admin
from .models import (RoomDetails, RoomPriceDetails, DrinkAndFood, BookingDetails, Photos, DrinkAndFoodOrder)


# Register your models here.
@admin.register(RoomDetails)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(BookingDetails)
class BookingAdmin(admin.ModelAdmin):
    list_select_related = True
    autocomplete_fields = ['guest']
    pass


@admin.register(RoomPriceDetails)
class RoomPriceAdmin(admin.ModelAdmin):
    pass


@admin.register(DrinkAndFood)
class DrinkAndFoodAdmin(admin.ModelAdmin):
    pass


@admin.register(DrinkAndFoodOrder)
class DrinkAndFoodOrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Photos)
class PhotoAdmin(admin.ModelAdmin):
    pass
