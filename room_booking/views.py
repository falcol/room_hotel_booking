import math

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
def booking_checkout(request, book_pk):
    try:
        book = BookingDetails.objects.get(pk=book_pk)
        if book.booking_type == 0:
            more_hours = math.ceil((book.check_out_time - book.check_in_time).seconds / 3600) - 2
            book.total_cost = book.room.room_price.price_first_two_hours + (
                more_hours * book.room.room_price.price_next_hours)
        if book.booking_type == 1:
            book.total_cost = book.room.room_price.price_per_night
        if book.booking_type == 2:
            book.total_cost = book.room.room_price.price_per_day
        book.booking_status = "TP"
    except BookingDetails.DoesNotExist:
        return redirect(request.META.get('HTTP_REFERER'))

    book_form = BookingCheckOutForms(request.POST or None, instance=book)
    if book_form.is_valid():
        book_form.save()
        return redirect("/home")

    context = {"form": book_form}

    return render(request, 'bookings/booking_checkout.html', context)
