from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import BadHeaderError
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from customer.models import CustomerDetails

from .forms import UserRegisterForm
from .models import User
from .tokens import generate_token

# Create your views here.


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = UserRegisterForm(request.POST or None)
    if request.method == "POST":

        if form.is_valid():
            form.save()
            username = request.POST.get('username')

            myuser = User.objects.get(username=username)

            myuser.is_active = False
            myuser.save()

            messages.success(request, "Kiểm tra email để kích hoạt tài khoản của bạn")

            # Welcome Email
            try:
                subject = "Đăng ký tài khoản thành công"
                message = "Xin chào " + myuser.username
                message += "\n Chào mừng bạn đến với website của chúng tôi"
                message += "\n Tôi sẽ gửi bạn email để xác nhận danh tính"
                message += "\n Xin hãy xác nhận lại trong email"
                from_email = settings.EMAIL_HOST_USER
                to_list = [myuser.email]
                send_mail(subject, message, from_email, to_list, fail_silently=True)

                # Email Address Confirmation Email

                current_site = get_current_site(request)
                email_subject = "Xác nhận đăng ký tài khoản!!"
                message2 = render_to_string(
                    'email_confirmation.html', {
                        'name': myuser.username,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                        'token': generate_token.make_token(myuser)
                    }
                )
                email = EmailMessage(
                    email_subject,
                    message2,
                    settings.EMAIL_HOST_USER,
                    [myuser.email],
                )
                email.fail_silently = True
                email.send()
            except BadHeaderError:
                print("Invalid header found")
            except SMTPException as e:
                print('Send mail error: ', e)
            except Exception:
                print("Send mail failed")

            return redirect('signin')

    context = {'register_form': form}

    return render(request, "signup.html", context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        detail = CustomerDetails.objects.create(customer_id=myuser)
        detail.save()
        login(request, myuser)
        messages.success(request, "Tài khoản của bạn đã được kích hoạt!!")
        return redirect('update_profile')
    else:
        return render(request, 'activation_failed.html')


next_redirect = ""


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    global next_redirect
    if request.GET.get('next'):
        next_redirect = request.GET.get('next')

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['password']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            messages.success(request, "Đăng nhập thành công!!")

            if next_redirect:
                return redirect(next_redirect)
            return redirect('home')
        else:
            messages.error(request, "Đăng nhập thất bại, thông tin tài khoản hoặc mật khẩu không chính xác!!")
            return redirect('home')

    return render(request, "signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Đăng xuất thành công!!")
    return redirect('home')
