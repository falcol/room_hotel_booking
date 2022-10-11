from tkinter.tix import Form
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

from room_booking.models import RoomDetails, BookingDetails
from room_booking.forms import BookingDetailsForms

# Create your views here.


@login_required(login_url='/signin')
def my_book(request):
    bookings = request.user.guest_bookings.all()

    context = {"bookings": bookings}
    return render(request, 'bookings/my_book.html', context)


def update_booking(request, pk):
    room_book = RoomDetails.objects.get(pk=pk)
    booking_pk = request.GET.get('bpk')
    try:
        booking = BookingDetails.objects.get(booking_id=booking_pk)
    except BookingDetails.DoesNotExist:
        pass

    form = BookingDetailsForms(request.POST or None, instance=booking)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhập lịch đặt phòng thành công')
            return redirect('my_book')

    context = {"form": form, "room_book": room_book}
    return render(request, 'bookings/update_book.html', context)
