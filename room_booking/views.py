from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from room_booking.models import BookingDetails, RoomDetails

from .forms import BookingCheckOutForms, BookingDetailsForms

# Create your views here.


@login_required(login_url='/signin')
def create_booking(request, pk):
    room_book = RoomDetails.objects.get(pk=pk)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = BookingDetailsForms(request.POST or None)

            if form.is_valid():
                booking = form.save(commit=False)
                booking.guest = request.user
                booking.hotel = room_book.hotel
                booking.room = room_book

                booking.save()
                messages.success(request, "Đặt phòng thành công")
                return redirect('home')
        return redirect('signin')
    else:
        form = BookingDetailsForms()

    context = {"form": form, "room_book": room_book}
    return render(request, 'bookings/booking_create.html', context)


@login_required(login_url='/signin')
def boooking_checkout(request, book_pk):
    try:
        book = BookingDetails.objects.get(pk=book_pk)
        # tinh tien
    except BookingDetails.DoesNotExist:
        return redirect(request.META.get('HTTP_REFERER'))
    book_form = BookingCheckOutForms(request.POST, instance=book)
    if request.method == 'POST':
        book_form.save()
