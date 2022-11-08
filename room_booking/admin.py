from django.contrib import admin

from .models import (
    BookingDetails,
    DrinkAndFood,
    DrinkAndFoodOrder,
    Photos,
    RoomDetails,
    RoomPriceDetails,
)


# Register your models here.
@admin.register(RoomDetails)
class RoomAdmin(admin.ModelAdmin):
    # form = RoomDetailsForms
    pass


@admin.register(BookingDetails)
class BookingAdmin(admin.ModelAdmin):
    # form = BookingDetailsForms
    list_select_related = True
    autocomplete_fields = ['guest']
    pass


@admin.register(RoomPriceDetails)
class RoomPriceAdmin(admin.ModelAdmin):
    # form = RoomPriceDetailsForms
    pass


@admin.register(DrinkAndFood)
class DrinkAndFoodAdmin(admin.ModelAdmin):
    # form = DrinkAndFoodForms
    pass


@admin.register(DrinkAndFoodOrder)
class DrinkAndFoodOrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Photos)
class PhotoAdmin(admin.ModelAdmin):
    pass
