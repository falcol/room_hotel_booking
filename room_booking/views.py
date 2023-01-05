import json
import math
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import redirect, render

from hotel_manager.models import HotelDetails
from room_booking.models import BookingDetails, DrinkAndFoodOrder, RoomDetails

from .forms import BookingCheckOutForms, BookingDetailsForms

# Create your views here.


@login_required(login_url='/signin')
def create_booking(request, pk):
    room_book = RoomDetails.objects.get(pk=pk)
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['room'] = room_book.pk
        request.POST['pre_order'] = True
        form = BookingDetailsForms(request.POST or None)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.guest = request.user
            booking.hotel = room_book.hotel
            booking.room = room_book

            booking.save()
            if request.user == room_book.hotel.owner:
                messages.success(request, "Đặt phòng thành công")
                return redirect('home')
            else:
                book_pre = BookingDetails.objects.get(booking_id=booking.booking_id)
                book_pre.pre_order = True
                book_pre.save()
                request.session['payment_status'] = 'booking'
                messages.success(request, "Đặt phòng thành công")
                return redirect("payment", book_pk=book_pre.booking_id)
    else:
        form = BookingDetailsForms()

    context = {"form": form, "room_book": room_book}
    return render(request, 'bookings/booking_create.html', context)


@login_required(login_url='/signin')
def staff_create_booking(request, pk):
    room_book = RoomDetails.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookingDetailsForms(request.POST or None)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.hotel = room_book.hotel
            booking.room = room_book

            booking.save()
            messages.success(request, "Đặt phòng thành công")
            return redirect('home')
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
                more_hours * book.room.room_price.price_next_hours
            )
        if book.booking_type == 1:
            book.total_cost = book.room.room_price.price_per_night
        if book.booking_type == 2:
            book.total_cost = book.room.room_price.price_per_day

        try:
            menu = DrinkAndFoodOrder.objects.filter(book=book).aggregate(Sum('amount'))
            book.total_cost = book.total_cost + menu['amount__sum']
        except TypeError:
            pass
        book.booking_status = "TP"
    except BookingDetails.DoesNotExist:
        return redirect(request.META.get('HTTP_REFERER'))

    book_form = BookingCheckOutForms(request.POST or None, instance=book)
    if request.method == 'POST':
        if book_form.is_valid():
            room = RoomDetails.objects.get(pk=book.room.pk)
            room.room_status = "E"
            room.save()
            book_form.save()
            if book_form.cleaned_data['refund'] is False:
                messages.success(request, "Trả phòng thành công")
                return redirect("home")
            request.session["refund_status"] = "hotel"
            return redirect("payment_refund", book_pk=book_pk)

    pay_online = None
    if book.pay_online is not None:
        pay_online = book.pay_online.amount

    room_name = book.room.room_name

    context = {"form": book_form, "pay_online": pay_online, "menu": menu['amount__sum'], "room_name": room_name}

    return render(request, 'bookings/booking_checkout.html', context)


@login_required(login_url='/signin')
def guest_check_in(request, book_pk):
    if request.method == 'POST':
        try:
            book = BookingDetails.objects.get(pk=book_pk)
            if book.pre_order:
                if book.pay_online is not None:
                    if book.pay_online.amount < 200000:
                        messages.warning(request, "Khách chưa đặt cọc đủ tiền phòng")
                        return redirect(request.path)
                    else:
                        book.booking_status = "NP"
                        book.room.room_status = "L"
                        book.room.save()
                        book.seen = True
                        book.save()
                        return redirect('my_hotel_book', hotel_pk=book.hotel.pk)
                else:
                    messages.warning(request, "Khách chưa đặt cọc đủ tiền phòng")
                    return redirect(request.path)
            book.booking_status = "NP"
            book.room.room_status = "L"
            book.room.save()
            book.seen = True
            book.save()
        except BookingDetails.DoesNotExist:
            pass
        return redirect('my_hotel_book', hotel_pk=book.hotel.pk)


@login_required(login_url='/signin')
def hotel_guest_cancel(request, book_pk):
    if request.method == 'POST':
        try:
            book = BookingDetails.objects.get(pk=book_pk)
            if datetime.now() < book.check_in_time:
                book.booking_status = "KSH"
                book.room.room_status = "E"
                book.room.save()
                book.seen = True
                book.save()
            else:
                return redirect('payment_refund', book_pk=book_pk)
        except BookingDetails.DoesNotExist:
            pass

        return redirect('my_hotel_book', hotel_pk=book.hotel.pk)


def booking_notify(request):
    user_pk = request.GET.get("user_pk")
    hotels = HotelDetails.objects.filter(owner__pk=user_pk).values('pk')
    books_all = BookingDetails.objects.filter(Q(hotel__pk__in=hotels) & Q(booking_status='DP') & Q(seen=False))
    count = books_all.count()
    books = books_all.values("booking_id", "hotel__name", "guest_name", "hotel__hotel_photos__image_hotel")
    return HttpResponse(json.dumps({"count": count, "books": list(books)}))


@login_required(login_url='/signin')
def redirect_notify(request, book_pk):
    if request.method == 'POST':
        try:
            book = BookingDetails.objects.get(pk=book_pk)
        except BookingDetails.DoesNotExist:
            pass
    return redirect('my_hotel_book', hotel_pk=book.hotel.pk)
