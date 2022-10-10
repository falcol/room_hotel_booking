from django.contrib import messages
from django.shortcuts import redirect, render

from room_booking.models import RoomDetails
from .forms import BookingDetailsForms

# Create your views here.


def create_booking(request, pk):
    room_book = RoomDetails.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookingDetailsForms(request.POST or None)

        if form.is_valid():
            form.save(commit=False)

            messages.success("Đặt phòng thành công")
            return redirect('home')
    else:
        form = BookingDetailsForms()

    context = {"form": form, "room_book": room_book}
    return render(request, 'bookings/booking_create.html', context)
