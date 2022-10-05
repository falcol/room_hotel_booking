from django.shortcuts import render
from .models import HotelDetails
from .forms import HotelCreateForm


# Create your views here.
def home(request):
    hotels = HotelDetails.objects.all()

    context = {"hotels": hotels}
    return render(request, "index.html", context)


def create_hotel(request):
    pass
