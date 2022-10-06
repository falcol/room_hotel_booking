from django.shortcuts import render

from .forms import HotelCreateForm
from .models import HotelDetails


# Create your views here.
def home(request):
    hotels = HotelDetails.objects.all()
    print(hotels)
    context = {"menu": "home", "hotels": hotels}
    return render(request, "hotels/index.html", context)


def create_hotel(request):
    hotel_create_form = HotelCreateForm(request.POST or None)

    if request.method == "POST":
        pass

    context = {"form": hotel_create_form, "menu": "hotel"}
    return render(request, 'hotels/create_hotel.html', context)
