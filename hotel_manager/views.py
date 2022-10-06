from django.shortcuts import redirect, render

from .forms import HotelCreateForm
from .models import HotelDetails
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from room_booking.forms import PhotoHotelForms


# Create your views here.
def home(request):
    print(request.META.get('HTTP_REFERER'))
    hotels = HotelDetails.objects.all()
    context = {"menu": "home", "hotels": hotels}
    return render(request, "hotels/index.html", context)


@login_required(login_url='/signin')
@user_passes_test(lambda user: user.is_staff or user.is_superuser)
def create_hotel(request):
    if request.method == "POST":
        hotel_create_form = HotelCreateForm(request.POST or None)
        photo_hotel_form = PhotoHotelForms(request.POST, request.FILES)
        print(request.POST, request.FILES)
        if hotel_create_form.is_valid() and photo_hotel_form.is_valid():
            new_hotel = hotel_create_form.save(commit=False)
            new_hotel.owner = request.user
            new_hotel.save()

            return redirect('home')
    else:
        hotel_create_form = HotelCreateForm()
        photo_hotel_form = PhotoHotelForms()

    context = {"form": hotel_create_form, "menu": "hotel", "file_form": photo_hotel_form}
    return render(request, 'hotels/create_hotel.html', context)
