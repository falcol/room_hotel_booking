import hashlib
import hmac
import urllib
import urllib.parse
import urllib.request
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render

from payment.models import Payment
from room_booking.models import BookingDetails
from websocket.redis_publish import publish_event

from .forms import PaymentForm
from .vnpay import vnpay


def index(request):
    return render(request, "index.html", {"title": "Danh sách demo"})


def hmacsha512(key, data):
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def payment(request, book_pk):
    form = PaymentForm(request.POST or None)
    money = request.GET.get("money")
    if money:
        request.session["payment_status"] = 'paid'
    try:
        check_status = request.session.get('payment_status', False)
    except KeyError:
        check_status = None
    if request.method == 'POST':
        # Process input data and build url payment
        if form.is_valid():
            order_type = form.cleaned_data['order_type']
            order_id = form.cleaned_data['order_id']
            amount = form.cleaned_data['amount'] * 100
            order_desc = form.cleaned_data['order_desc']
            bank_code = form.cleaned_data['bank_code']
            language = form.cleaned_data['language']
            ipaddr = get_client_ip(request)
            # Build URL Payment
            vnp = vnpay()
            vnp.requestData['vnp_Version'] = '2.1.0'
            vnp.requestData['vnp_Command'] = 'pay'
            vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
            vnp.requestData['vnp_Amount'] = amount
            vnp.requestData['vnp_CurrCode'] = 'VND'
            vnp.requestData['vnp_TxnRef'] = order_id
            vnp.requestData['vnp_OrderInfo'] = order_desc
            vnp.requestData['vnp_OrderType'] = order_type
            # Check language, default: vn
            if language and language != '':
                vnp.requestData['vnp_Locale'] = language
            else:
                vnp.requestData['vnp_Locale'] = 'vn'
                # Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
            if bank_code and bank_code != "":
                vnp.requestData['vnp_BankCode'] = bank_code

            vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')    # 20150410063022
            vnp.requestData['vnp_IpAddr'] = ipaddr
            vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL + f"?book_pk={book_pk}"
            vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
            print(vnpay_payment_url)

            try:
                book = BookingDetails.objects.get(booking_id=book_pk)
                if book.pay_online is None:
                    pay = Payment()
                    pay.order_id = order_id
                    pay.order_type = order_type
                    pay.amount = 0
                    pay.order_desc = order_desc
                    pay.bank_code = bank_code
                    pay.language = language
                    pay.save()
                    book.pay_online = pay

                book.pre_order = True
                book.save()
            except BookingDetails.DoesNotExist:
                pass

            return redirect(vnpay_payment_url, book_pk=book_pk)
        else:
            context = {"title": "Thanh toán", "book_pk": book_pk, "form": form, "check_status": check_status}
            return render(request, "payment.html", context)
    else:
        context = {
            "title": "Thanh toán",
            "book_pk": book_pk,
            "form": form,
            "check_status": check_status,
            "money": money
        }
        return render(request, "payment.html", context)


def payment_ipn(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = inputData['vnp_Amount']
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            # Check & Update Order Status in your Database
            # Your code here
            firstTimeUpdate = True
            totalamount = True
            if totalamount:
                if firstTimeUpdate:
                    if vnp_ResponseCode == '00':
                        print('Payment Success. Your code implement here')
                    else:
                        print('Payment Error. Your code implement here')

                    # Return VNPAY: Merchant update success
                    result = JsonResponse({'RspCode': '00', 'Message': 'Confirm Success'})
                else:
                    # Already Update
                    result = JsonResponse({'RspCode': '02', 'Message': 'Order Already Update'})
            else:
                # invalid amount
                result = JsonResponse({'RspCode': '04', 'Message': 'invalid amount'})
        else:
            # Invalid Signature
            result = JsonResponse({'RspCode': '97', 'Message': 'Invalid Signature'})
    else:
        result = JsonResponse({'RspCode': '99', 'Message': 'Invalid request'})

    return result


def payment_return(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        book_pk = inputData['book_pk']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                hotel_owner = ""
                if book_pk and request.session.get("payment_status", False) == 'paid':
                    book = BookingDetails.objects.get(booking_id=book_pk)
                    book.total_cost = book.pay_online.amount + amount
                    book.booking_status = "TP"
                    book.room.room_status = "E"
                    book.room.save()
                    book.is_pay = True
                    book.pay_online.amount = book.pay_online.amount + amount
                    book.pay_online.save()
                    book.save()
                    hotel_owner = book.hotel.owner.pk
                    messages.success(request, "Thanh toán phòng thành công")

                if book_pk and request.session.get("payment_status", False) == 'booking':
                    book = BookingDetails.objects.get(booking_id=book_pk)
                    if book.pay_online is not None:
                        book.pay_online.amount = book.pay_online.amount + amount
                        book.pay_online.save()
                        book.save()
                        hotel_owner = book.hotel.owner.pk
                        messages.success(request, "Đặt phòng thành công")

                event = {"event_type": "reload_notify", "payload": {"user_id": hotel_owner}}
                channel = f"notify_{hotel_owner}"
                publish_event(channel=channel, event=event)

                request.session['payment_status'] = ''
                return render(
                    request, "payment_return.html", {
                        "title": "Kết quả thanh toán",
                        "result": "Thành công",
                        "order_id": order_id,
                        "amount": amount,
                        "order_desc": order_desc,
                        "vnp_TransactionNo": vnp_TransactionNo,
                        "vnp_ResponseCode": vnp_ResponseCode,
                        "book_pk": book_pk
                    }
                )
            else:
                return render(
                    request, "payment_return.html", {
                        "title": "Kết quả thanh toán",
                        "result": "Lỗi",
                        "order_id": order_id,
                        "amount": amount,
                        "order_desc": order_desc,
                        "vnp_TransactionNo": vnp_TransactionNo,
                        "vnp_ResponseCode": vnp_ResponseCode,
                        "book_pk": book_pk
                    }
                )
        else:
            return render(
                request, "payment_return.html", {
                    "title": "Kết quả thanh toán",
                    "result": "Lỗi",
                    "order_id": order_id,
                    "amount": amount,
                    "order_desc": order_desc,
                    "vnp_TransactionNo": vnp_TransactionNo,
                    "vnp_ResponseCode": vnp_ResponseCode,
                    "msg": "Sai checksum"
                }
            )
    else:
        return render(request, "payment_return.html", {"title": "Kết quả thanh toán", "result": ""})


def query(request):
    if request.method == 'GET':
        return render(request, "query.html", {"title": "Kiểm tra kết quả giao dịch"})
    else:
        # Add paramter
        vnp = vnpay()
        vnp.requestData = {}
        vnp.requestData['vnp_Command'] = 'querydr'
        vnp.requestData['vnp_Version'] = '2.1.0'
        vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
        vnp.requestData['vnp_TxnRef'] = request.POST['order_id']
        vnp.requestData['vnp_OrderInfo'] = 'Kiem tra ket qua GD OrderId:' + request.POST['order_id']
        vnp.requestData['vnp_TransDate'] = request.POST['trans_date']    # 20150410063022
        vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')    # 20150410063022
        vnp.requestData['vnp_IpAddr'] = get_client_ip(request)
        requestUrl = vnp.get_payment_url(settings.VNPAY_API_URL, settings.VNPAY_HASH_SECRET_KEY)
        responseData = urllib.request.urlopen(requestUrl).read().decode()
        print('RequestURL:' + requestUrl)
        print('VNPAY Response:' + responseData)
        data = responseData.split('&')
        for x in data:
            tmp = x.split('=')
            if len(tmp) == 2:
                vnp.responseData[tmp[0]] = urllib.parse.unquote(tmp[1]).replace('+', ' ')

        # print('Validate data from VNPAY:' + str(vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY)))
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if request.session.get("refund_status", False) == "guest":
                book_pk = int(request.session.get("book_pk", False))
                try:
                    book = BookingDetails.objects.filter(booking_id=book_pk).first()
                    book.booking_status = "KH"
                    book.room.room_status = "E"
                    book.seen = True
                    book.room.save()
                    book.save()
                    messages.success(request, "Thanh toán hoàn trả thành công")
                    del request.session['refund_status']
                except BookingDetails.DoesNotExist:
                    messages.error(request, "Không có thông tin đặt phòng")
                    return redirect("my_book")

            if request.session.get("refund_status", False) == "hotel":
                book_pk = int(request.session.get("booking_pk", False))
                book = BookingDetails.objects.filter(booking_id=book_pk).first()
                book.is_pay = True
                book.room.room_status = "E"
                book.room.save()
                book.save()
                del request.session['refund_status']
                del request.session['booking_pk']

            if request.session.get("book_out", False) == "True":
                book_pk = int(request.session.get("book_pk", False))
                book = BookingDetails.objects.filter(booking_id=book_pk).first()
                book.booking_status = "KSH"
                book.room.room_status = "E"
                book.room.save()
                book.seen = True
                book.save()
                hotel_owner = book.hotel.owner.pk
                event = {"event_type": "reload_notify", "payload": {"user_id": hotel_owner}}
                channel = f"notify_{hotel_owner}"
                publish_event(channel=channel, event=event)
                del request.session["book_out"]
                del request.session["book_pk"]

            if request.session.get("book_guest_out", False) == "True":
                book_pk = int(request.session.get("book_pk", False))
                book = BookingDetails.objects.filter(booking_id=book_pk).first()
                book.booking_status = "KH"
                book.room.room_status = "E"
                book.seen = True
                book.room.save()
                book.save()
                hotel_owner = book.hotel.owner.pk
                event = {"event_type": "reload_notify", "payload": {"user_id": hotel_owner}}
                channel = f"notify_{hotel_owner}"
                publish_event(channel=channel, event=event)
                del request.session["book_guest_out"]
                del request.session["book_pk"]

                messages.success(request, "Thanh toán hoàn trả thành công")
            messages.success(request, "Thanh toán hoàn trả thành công")

        return render(request, "query.html", {"title": "Kiểm tra kết quả giao dịch", "data": vnp.responseData})


@login_required(login_url='/signin')
def refund(request, book_pk):
    if book_pk is None:
        return redirect("home")
    book = BookingDetails.objects.get(booking_id=book_pk)
    check_owner = False
    if request.user == book.hotel.owner:
        check_owner = True
    if book.pay_online is None:
        if request.user.pk is not book.hotel.owner.pk:
            book_pk = int(request.session.get("book_pk", False))
            if book_pk:
                book = BookingDetails.objects.filter(booking_id=book_pk).first()
                book.booking_status = "KH"
                book.room.room_status = "E"
                book.room.save()
                book.seen = True
                book.save()
                hotel_owner = book.hotel.owner.pk
                event = {"event_type": "reload_notify", "payload": {"user_id": hotel_owner}}
                channel = f"notify_{hotel_owner}"
                publish_event(channel=channel, event=event)
                del request.session["book_out"]
                del request.session["book_pk"]
            messages.warning(request, "Không có hóa đơn")
        else:
            if request.session.get("book_out", False) == "True":
                book_pk = int(request.session.get("book_pk", False))
                book = BookingDetails.objects.filter(booking_id=book_pk).first()
                book.booking_status = "KSH"
                book.room.room_status = "E"
                book.room.save()
                book.seen = True
                book.save()
                hotel_owner = book.hotel.owner.pk
                event = {"event_type": "reload_notify", "payload": {"user_id": hotel_owner}}
                channel = f"notify_{hotel_owner}"
                publish_event(channel=channel, event=event)
                del request.session["book_out"]
                del request.session["book_pk"]
            messages.success(request, "Trả phòng thành công")
        return redirect('home')

    money_refund = book.pay_online.amount * 90 / 100
    if request.session.get("book_out", False) == "True" or request.session.get(
            "book_guest_out", False) == "True" or book.check_in_time < datetime.now():
        money_refund = book.pay_online.amount

    context = {"title": "Gửi yêu cầu hoàn tiền", "book": book, "check_owner": check_owner, "money_refund": money_refund}
    return render(request, "refund.html", context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
