from datetime import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.shortcuts import redirect, render

from common.vietnam_province import VIETNAM_CITY
from room_booking.forms import (
    PhotoForms,
    RoomDetailsForms,
    RoomPriceDetailsForms,
    SearchRoomsEmty,
    UpdatePhotoRoom,
)
from room_booking.models import BookingDetails, Photos, RoomDetails, RoomPriceDetails

from .forms import HotelCreateForm, UpdatePhotoHotel
from .models import HotelDetails


# Create your views here.
def home(request):
    hotels = HotelDetails.objects.all().order_by("-id")
    if request.method == "POST":
        form = SearchRoomsEmty(request.POST)
        if form.is_valid():
            data_search = form.cleaned_data
            time_start = data_search.get('datetime_check_in')
            time_end = data_search.get('datetime_check_out')
            max_person = data_search.get('max_person')

            books_room = BookingDetails.objects.filter(
                (~Q(booking_status__contains='DP') | ~Q(booking_status__contains="NP")) &
                (Q(check_in_time__range=[time_start, time_end]) |
                 Q(check_out_time__range=[time_start, time_end]))).values('room__id')
            id_book_rooms = [room["room__id"] for room in books_room]
            all_rooms = RoomDetails.objects.filter(room_price__max_person__gte=max_person).exclude(id__in=id_book_rooms)
            hotel_ids = all_rooms.values('hotel__id').annotate(room_count=Count('hotel__id')).filter(room_count__gte=1)
            hotels = HotelDetails.objects.filter(pk__in=[item['hotel__id'] for item in hotel_ids])
            print(hotel_ids)
            pass
    else:
        form = SearchRoomsEmty()
    context = {"menu": "home", "hotels": hotels, 'search_form': form}
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


@login_required(login_url='/signin')
@user_passes_test(lambda user: user.is_staff or user.is_superuser)
def my_hotels(request):
    hotels = request.user.hotels.all()

    context = {'hotels': hotels}
    return render(request, 'hotels/my_hotels.html', context)


def hotel_rooms(request, pk):
    room_prices = RoomPriceDetails.objects.filter(hotel__id=pk)

    rooms = RoomDetails.objects.filter(hotel__pk=pk)

    context = {"room_prices": room_prices, "rooms": rooms}
    return render(request, 'rooms/rooms_hotel.html', context)


@login_required(login_url='/signin')
def my_hotel_rooms(request, pk):
    room_prices = RoomPriceDetails.objects.filter(hotel__id=pk)

    rooms = RoomDetails.objects.filter(hotel__pk=pk)

    context = {"room_prices": room_prices, "rooms": rooms}
    return render(request, 'rooms/my_rooms_hotel.html', context)


@login_required(login_url='/signin')
def create_room_price(request, hotel_pk):
    hotel = HotelDetails.objects.get(pk=hotel_pk)

    if request.method == 'POST':
        form = RoomPriceDetailsForms(request.POST or None)
        if form.is_valid():
            room_price = form.save(commit=False)
            room_price.hotel = hotel
            room_price.save()

            return redirect('list_room_price', hotel_pk=hotel_pk)
    else:
        form = RoomPriceDetailsForms()

    context = {"form": form, "screen": 'hotel'}

    return render(request, 'rooms/create_room_price.html', context)


@login_required(login_url='/signin')
def list_room_price(request, hotel_pk):
    try:
        room_prices = RoomPriceDetails.objects.filter(hotel__pk=hotel_pk)
    except RoomPriceDetails.DoesNotExist:
        room_prices = []
    context = {"room_prices": room_prices}

    return render(request, 'rooms/list_room_price.html', context)


@login_required(login_url='/signin')
def update_room_price(request, room_price_pk):
    room_price = RoomPriceDetails.objects.get(pk=room_price_pk)

    form = RoomPriceDetailsForms(request.POST or None, instance=room_price)
    if request.method == "POST":
        if form.is_valid():
            form.save()

            return redirect('list_room_price', hotel_pk=room_price.hotel.pk)

    context = {"form": form, "room_price_name": room_price.room_type}
    return render(request, "rooms/update_room_price.html", context)


@login_required(login_url='/signin')
def create_room_hotel(request, hotel_pk):
    room_prices = RoomPriceDetails.objects.filter(hotel__pk=hotel_pk)

    if request.method == 'POST':
        form = RoomDetailsForms(request.POST or None)
        photo = PhotoForms(request.POST, request.FILES)

        if form.is_valid() and photo.is_valid():
            new_room = form.save(commit=False)
            hotel = HotelDetails.objects.get(pk=hotel_pk)
            new_room.hotel = hotel
            new_room.save()

            images = request.FILES.getlist('images')
            for image in images:
                photo = Photos.objects.create(room_id=new_room, image_room=image, image_name=image.name)
                photo.save()

            return redirect('hotel_rooms', pk=hotel_pk)
    else:
        form = RoomDetailsForms()
        photo = PhotoForms()
    context = {"form": form, "photo_form": photo, "room_prices": room_prices, "hotel_pk": hotel_pk, "screen": 'hotel'}

    return render(request, 'rooms/create_room.html', context)


@login_required(login_url='/signin')
def update_room_hotel(request, room_pk):
    try:
        room = RoomDetails.objects.get(pk=room_pk)
        room_prices = RoomPriceDetails.objects.filter(hotel__pk=room.hotel.pk)
        photo = Photos.objects.filter(room_id=room_pk).first()
    except (RoomDetails.DoesNotExist, RoomPriceDetails.DoesNotExist, Photos.DoesNotExist):
        pass

    form = RoomDetailsForms(request.POST or None, instance=room)
    photo_form = UpdatePhotoRoom(request.POST, request.FILES, instance=photo)
    if photo_form.is_valid():
        photo_form.save()

    if form.is_valid():
        form.save()
        return redirect('my_hotel_rooms', pk=room.hotel.pk)

    context = {"form": form, 'screen': 'room', "room_prices": room_prices, "photo_form": photo_form, "room": room}

    return render(request, 'rooms/update_room.html', context)


@login_required(login_url='/signin')
def update_hotel_info(request, hotel_pk):
    try:
        hotel = HotelDetails.objects.get(pk=hotel_pk)
        photo = Photos.objects.filter(hotel_id=hotel_pk).first()
    except HotelDetails.DoesNotExist:
        pass

    form = HotelCreateForm(request.POST or None, instance=hotel)
    photo_form = UpdatePhotoHotel(request.POST, request.FILES, instance=photo)
    if photo_form.is_valid():
        photo_form.save()

    if form.is_valid():
        form.save()
        return redirect("my_hotel")
    context = {'form': form, "photo_form": photo_form}
    return render(request, "hotels/update_hotel.html", context)


@login_required(login_url='/signin')
def my_hotel_book(request, hotel_pk):
    hotel_books = BookingDetails.objects.filter(Q(hotel=hotel_pk) & (Q(booking_status="DP") | Q(booking_status="NP")))
    context = {"books": hotel_books}
    return render(request, 'hotels/my_hotel_books.html', context)


@login_required(login_url='/signin')
def set_room_empty(request, room_pk):
    try:
        room = RoomDetails.objects.get(pk=room_pk)
        room.room_status = "E"
    except RoomDetails.DoesNotExist:
        pass

    return redirect(request.path)


@login_required(login_url='/signin')
def dashboard(request, hotel_pk):
    books = BookingDetails.objects.filter(hotel__pk=hotel_pk, booking_status="TP")
    books_month = books.annotate(month=TruncMonth('check_in_time')).values('month').annotate(
        total_cost=Sum('total_cost'), total_book=Count('pk')).order_by()
    book_all = books.aggregate(Sum('total_cost'), Count('pk'))
    cost_day = BookingDetails.objects.filter(
        hotel__pk=hotel_pk, booking_status="TP",
        created_at__date=datetime.date(datetime.now())).aggregate(Sum('total_cost'))['total_cost__sum']
    total_rooms = RoomDetails.objects.filter(hotel__pk=hotel_pk).count()
    books_year = books.annotate(year=TruncYear('check_in_time')).values('year').annotate(
        total_cost=Sum('total_cost'), total_book=Count('pk')).order_by()

    context = {"books_month": books_month, "total_rooms": total_rooms, "cost_day": cost_day, "books_year": books_year}
    context.update(book_all)
    return render(request, 'hotels/dashboard.html', context)
