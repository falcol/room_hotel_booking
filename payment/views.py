import hashlib
import hmac
import urllib
import urllib.parse
import urllib.request
from datetime import datetime

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import PaymentForm
from .vnpay import vnpay


def index(request):
    return render(request, "index.html", {"title": "Danh sách demo"})


def hmacsha512(key, data):
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def payment(request):

    if request.method == 'POST':
        # Process input data and build url payment
        form = PaymentForm(request.POST)
        if form.is_valid():
            order_type = form.cleaned_data['order_type']
            order_id = form.cleaned_data['order_id']
            amount = form.cleaned_data['amount']
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
            vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
            vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
            print(vnpay_payment_url)
            return redirect(vnpay_payment_url)
        else:
            print("Form input not validate")
    else:
        return render(request, "payment.html", {"title": "Thanh toán"})


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
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                return render(
                    request, "payment_return.html", {
                        "title": "Kết quả thanh toán",
                        "result": "Thành công",
                        "order_id": order_id,
                        "amount": amount,
                        "order_desc": order_desc,
                        "vnp_TransactionNo": vnp_TransactionNo,
                        "vnp_ResponseCode": vnp_ResponseCode
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
                        "vnp_ResponseCode": vnp_ResponseCode
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

        print('Validate data from VNPAY:' + str(vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY)))
        return render(request, "query.html", {"title": "Kiểm tra kết quả giao dịch", "data": vnp.responseData})


def refund(request):
    return render(request, "refund.html", {"title": "Gửi yêu cầu hoàn tiền"})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
