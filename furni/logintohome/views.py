from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime
from .models import CustomUser1
from . import models
from django.contrib import messages
from django.views.decorators.cache import never_cache
from afterlogin.models import cart, wishlist
from userprofile.models import wallet
import uuid
from product_manage.models import products



# Create your views here.
# home
@never_cache
def index(request):
    items = products.objects.filter(is_listed=True, category__is_listed=True).order_by(
        "-id"
    )[:3]

    if "email" in request.session:
        email1 = request.session["email"]
        obj = CustomUser1.objects.get(email=email1)
        id = obj.id
        no = cart.objects.filter(user_id=id).count()
        no1 = wishlist.objects.filter(user_id=id).count()
        items = products.objects.filter(
            is_listed=True, category__is_listed=True
        ).order_by("-id")[:3]

        context = {"no": no, "no1": no1, "items": items}
        if obj.is_blocked:
            messages.error(request, "you are blocked")
            request.session.flush()
            return redirect("userlogin")
        else:
            return render(request, "home.html", context)
    return render(request, "home.html", {"items": items})


# user login
@never_cache
def user_login(request):
    if "email" in request.session:
        return redirect("index")
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["pass"]
        try:
            user = CustomUser1.objects.get(email=email, password=password)
        except:
            user = None
        if user is not None:
            if user.is_blocked:
                messages.error(request, "you are blocked")
                return redirect("userlogin")
            if user.is_verified:
                request.session["email"] = email
                messages.success(request, f"welcome to our world   {user.username}")
                return redirect("index")
            else:
                p = models.generate_otp(user)
                models.send_otp_email(user, p)
                return redirect("otpverification", user.id)

        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "user_login.html")


# user signup
@never_cache
def user_signup(request):
    if "email" in request.session:
        return redirect("index")
    link = request.GET.get("ref", "w")
    context = {"link": link}
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["pass"]
        phone = request.POST["phone"]
        current_date = timezone.now().date()
        if CustomUser1.objects.filter(email=email).exists():
            messages.error(request, "email already exists change your email")
            return redirect("usersignup")
        if len(phone) == 10 and int(phone) > 0:
            unique_code = str(uuid.uuid4().hex)[:10]
            y = unique_code
            user1 = CustomUser1(
                username=username,
                email=email,
                password=password,
                phone=phone,
                date_joined=current_date,
                referral_link=y,
            )
            if len(link) == 10:
                refered_user = CustomUser1.objects.get(referral_link=link)
                print(refered_user.username)
                waluser = wallet.objects.get(user_id=refered_user)
                waluser.amount = waluser.amount + 1000
                waluser.save()
            user1.save()
            wallet.objects.create(user_id_id=user1.id, amount=0)
            return redirect("otpverification", id=user1.id)
        else:
            messages.error(request, "the phone number should valid")
            return render(request, "user_signup.html", context)
    return render(request, "user_signup.html", context)


# otp verification
@never_cache
def otp_verification(request, id):
    if request.method == "POST":
        otp1 = CustomUser1.objects.get(id=id)
        p = otp1.otp_fld
        entered_otp = request.POST.get("o1")
        p = int(p)
        entered_otp = int(entered_otp)
        if entered_otp == p:
            user1 = CustomUser1.objects.get(id=id)
            user1.is_verified = True
            user1.save()
            messages.success(
                request, "Email verified successfully. You can now log in."
            )
            return redirect("userlogin")

        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("otpverification", id)

    return render(request, "otp_verification.html")


# logout
@never_cache
def logout(request):
    if "email" in request.session:
        request.session.flush()
    return redirect("userlogin")


# reset password
def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = CustomUser1.objects.get(email=email)
        except:
            user = None
        if user is not None:
            p = models.generate_otp(user)
            models.send_otp_email(user, p)
            return redirect("resetpassotp", p, user.id)
        else:
            messages.error(request, "you have no account.....please signup")
            return redirect("usersignup")

    return render(request, "reset_password.html")


# otp verification for reset password
def reset_pass_otp(request, otp, id):
    user_id = id
    if request.method == "POST":
        entrd_otp = request.POST["o1"]
        if otp == entrd_otp:
            return redirect("confirmpassword", user_id)
        else:
            messages.error(request, "enter correct otp")
    return render(request, "reset_password_otp.html")


# reset your password here
def confirm_password(request, id):
    if request.method == "POST":
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]
        if pass1 == pass2:
            obj = CustomUser1.objects.get(id=id)
            obj.password = pass1
            obj.save()
            messages.success(request, "password changed successfully")
            return redirect("userlogin")
        else:
            messages.error(request, "the password should be same")

    return render(request, "confirm_password.html")


# about us
def about_us(request):
    return render(request, "aboutus.html")


# contact us
def contact_us(request):
    return render(request, "contactus.html")
