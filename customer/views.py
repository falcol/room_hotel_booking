import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from common.vietnam_province import VIETNAM_CITY
from middleware.paginator import paginator_list_function
from room_booking.forms import BookingDetailsForms
from room_booking.models import (
    BookingDetails,
    DrinkAndFood,
    DrinkAndFoodOrder,
    RoomDetails,
)

from .forms import CustomerDetailsForm, UserInfoForm
from .models import Comments, RatingStars

# Create your views here.


@login_required(login_url='/signin')
def my_book(request):
    bookings = request.user.guest_bookings.filter(Q(booking_status="DP") | Q(booking_status="NP"))

    context = {"bookings": bookings}
    return render(request, 'bookings/my_book.html', context)


@login_required(login_url='/signin')
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


@login_required(login_url='/signin')
def guest_cancel(request, book_pk):
    if request.method == 'POST':
        try:
            book = BookingDetails.objects.get(pk=book_pk)
            book.booking_status = "KH"
            book.room.room_status = "E"
            book.seen = True
            book.save()
            messages.success(request, "Hủy phòng thanh công")
        except BookingDetails.DoesNotExist:
            pass

        return redirect('my_book')


@login_required(login_url='/signin')
def my_profile(request):
    user_form = UserInfoForm(request.POST or None, instance=request.user)
    detail_form = CustomerDetailsForm(request.POST or None, instance=request.user.info.first())

    if request.method == "POST":

        if user_form.is_valid() and detail_form.is_valid():
            user_form.save()
            detail_form.save()

            messages.success(request, "Cập nhập thông tin thành công")
            return redirect("home")

    context = {"user_form": user_form, "detail_form": detail_form, "vietnam_city": VIETNAM_CITY}

    return render(request, "customer/update.html", context)


def create_comment(request):
    if request.method == 'POST':
        room_pk = request.POST.get("room_pk")
        cmt = request.POST.get('comment')
        if room_pk and cmt:
            try:

                room = RoomDetails.objects.get(pk=room_pk)
                comment = Comments.objects.create(room=room, hotel=room.hotel, user=request.user, comment=cmt)
                comment.save()

                response = {
                    "comment": cmt,
                    "c_date": comment.created_at.strftime("%d/%m/%Y"),
                    "user": comment.user.username or comment.user.name,
                }

                return HttpResponse(json.dumps(response))
            except Exception as e:
                return HttpResponse(json.dumps({
                    "comments": None,
                    "error": e.args,
                }))

    return HttpResponse(json.dumps({
        "comments": None,
        "error": "Method not allowed",
    }))


def create_rating(request):
    if request.method == 'POST':
        room_pk = request.POST.get("room_pk")
        rating = request.POST.get('rating')
        if room_pk and rating:
            try:
                room = RoomDetails.objects.get(pk=room_pk)
                obj, create = RatingStars.objects.update_or_create(
                    room=room, hotel=room.hotel, user=request.user, defaults={"rating": float(rating)}
                )
                if create:
                    obj.save()

                room.rating_star = float(rating)
                room.save()

                hotel_star = RatingStars.objects.filter(hotel=room.hotel).aggregate(Avg("rating"))
                room.hotel.rating_star = hotel_star['rating__avg']
                room.hotel.save()

                response = {
                    "rating": rating,
                }

                return HttpResponse(json.dumps(response))
            except Exception as e:
                return HttpResponse(json.dumps({
                    "rating": None,
                    "error": e.args,
                }))

    return HttpResponse(json.dumps({
        "rating": None,
        "error": "Method not allowed",
    }))


def load_comments(request):
    room_pk = request.GET.get("room_pk")
    comments = Comments.objects.filter(room__pk=room_pk).order_by("-pk").values(
        "comment", "created_at__year", "created_at__month", "created_at__day", "user__username", "user__name"
    )
    page_number = request.GET.get("page", 1)
    comments = paginator_list_function(comments, page_number)

    next_page = None
    previous_page = None
    if comments.has_next():
        next_page = comments.next_page_number()
    if comments.has_previous():
        previous_page = comments.previous_page_number()

    return HttpResponse(
        json.dumps(
            {
                "comment": list(comments),
                "pages": comments.paginator.num_pages,
                "previous": previous_page,
                "next": next_page,
                "this_page": comments.number,
                "per_page": comments.paginator.per_page,
            }
        )
    )


@login_required(login_url='/signin')
def get_menu(request, hotel_pk):
    menus = DrinkAndFood.objects.filter(hotel_pk__pk=hotel_pk).order_by("item_name")
    context = {"menus": menus}
    return render(request, "menu/list_order.html", context)


def order_menu(request, book_pk):
    if request.method == "POST":
        menu_id = request.POST.get("menu_id")
        total = request.POST.get("total")
        if menu_id:
            try:
                menu = DrinkAndFood.objects.get(pk=menu_id)
                book = BookingDetails.objects.get(pk=book_pk)
                new_order, _ = DrinkAndFoodOrder.objects.update_or_create(drink_and_food=menu, book=book)

                new_order.total = int(total)
                new_order.amount = menu.price * int(total)
                new_order.save()

                response = {"sucess": True}

                return HttpResponse(json.dumps(response))

            except DrinkAndFood.DoesNotExist:
                return None
        pass

    return None
