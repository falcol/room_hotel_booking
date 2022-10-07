from common.vietnam_province import VIETNAM_CITY
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from room_booking.forms import PhotoForms
from room_booking.models import Photos, RoomPriceDetails, RoomDetails

from .forms import HotelCreateForm
from .models import HotelDetails


# Create your views here.
def home(request):
    hotels = HotelDetails.objects.all()
    context = {"menu": "home", "hotels": hotels}
    return render(request, "hotels/index.html", context)


@login_required(login_url='/signin')
@user_passes_test(lambda user: user.is_staff or user.is_superuser)
def create_hotel(request):
    if request.method == "POST":
        hotel_create_form = HotelCreateForm(request.POST or None)
        photo_hotel_form = PhotoForms(request.POST, request.FILES)

        if hotel_create_form.is_valid() and photo_hotel_form.is_valid():
            new_hotel = hotel_create_form.save(commit=False)
            new_hotel.owner = request.user
            new_hotel.save()
            images = request.FILES.getlist('images')
            for image in images:
                photo = Photos.objects.create(hotel_id=new_hotel, image_hotel=image, image_name=image.name)
                photo.save()
                pass

            return redirect('home')
    else:
        hotel_create_form = HotelCreateForm()
        photo_hotel_form = PhotoForms()

    context = {"form": hotel_create_form, "menu": "hotel", "file_form": photo_hotel_form, "vietnam_city": VIETNAM_CITY}

    return render(request, 'hotels/create_hotel.html', context)


def hotel_rooms(request, pk):
    room_prices = RoomPriceDetails.objects.filter(hotel__id=pk)

    rooms = RoomDetails.objects.filter(hotel__pk=pk)

    context = {"room_prices": room_prices, "rooms": rooms}
    return render(request, 'hotels/rooms_hotel.html', context)
