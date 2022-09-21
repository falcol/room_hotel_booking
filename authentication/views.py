from django.http import BadHeaderError
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from .tokens import generate_token
from .forms import UserRegisterForm
from django.conf import settings
from smtplib import SMTPException


# Create your views here.
def home(request):
    return render(request, "authentication/index.html")


def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        print(form.error_messages)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')

            myuser = User.objects.get(username=username)

            myuser.is_active = False
            myuser.save()
            print(myuser)
            messages.success(
                request,
                "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account."
            )

            # Welcome Email
            try:
                subject = "Welcome to GFG- Django Login!!"
                message = "Hello " + myuser.username + "!! \n" + "Welcome to GFG!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnubhav Madhav"
                from_email = settings.EMAIL_HOST_USER
                to_list = [myuser.email]
                send_mail(subject,
                          message,
                          from_email,
                          to_list,
                          fail_silently=True)

                # Email Address Confirmation Email

                current_site = get_current_site(request)
                email_subject = "Confirm your Email @ GFG - Django Login!!"
                message2 = render_to_string(
                    'email_confirmation.html', {
                        'name': myuser.username,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                        'token': generate_token.make_token(myuser)
                    })
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
                print('Send mail error: ' + e)
            except:
                print("Send mail failed")

            return redirect('signin')
    else:
        form = UserRegisterForm()

    context = {'register_form': form}

    return render(request, "authentication/signup.html", context)


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
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request, 'activation_failed.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "authentication/index.html",
                          {"fname": fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')
