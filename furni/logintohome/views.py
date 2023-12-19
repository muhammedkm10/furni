from django.shortcuts import render,redirect
from django.utils import timezone
from datetime import datetime
from . models import CustomUser1,otpverification
from .import models
from django.contrib import messages
from django.views.decorators.cache import never_cache




# Create your views here.
# home 
@never_cache
def index(request):
        
            email1 = request.session.get('email')
            print(email1)
            try:
             user4 = CustomUser1.objects.get(email = email1)
            except:
                print("hai")
                return render(request,'home.html')
            if user4.is_verified:
                 return render (request,'home.html')
            else:
                CustomUser1.objects.get(email =email1).delete()
            return render(request,'home.html')
        

# user login
@never_cache
def user_login(request):
    if 'email' in request.session:
        return redirect('index')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        try:
           user = CustomUser1.objects.get(email = email,password = password,is_verified=True)
        except:
            user = None
        if user is not None:
            request.session['email'] = email
            messages.success(request, "welcome to our world")
            return redirect('index')
        else:
            messages.error(request, "Invalid email or password.or not verified Please try again.")
    return render (request,'user_login.html')



# user signup
def user_signup(request):
    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass']
        phone = request.POST['phone']
        current_date = timezone.now().date()
        if CustomUser1.objects.filter(email=email).exists():
            messages.error(request, "email already exists change your email")
            return redirect('usersignup')
        user1  = CustomUser1(username = username,email = email,password = password,phone = phone,date_joined=current_date)
        user1.save()
        return redirect('otpverification',id=user1.id)
    return render (request,'user_signup.html')



# otp verification
@never_cache
def otp_verification(request,id):
     
    if request.method == 'POST': 
        otp1 = otpverification.objects.get(user_id=id)
        p = otp1.otp_nuber
        print(p)
        entered_otp = request.POST.get('o1')
        print(entered_otp)
        p = int(p)
        entered_otp = int(entered_otp)
        if entered_otp == p:  
            user1 = CustomUser1.objects.get(id=id)
            user1.is_verified = True
            user1.save()
            messages.success(request, "Email verified successfully. You can now log in.")
            return redirect('userlogin') 

        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return render(request, 'user_signup.html')

    
    return render (request,'otp_verification.html')
    

 
# logout
@never_cache
def logout(request):
    if 'email' in request.session:
        request.session.flush()
    return redirect('userlogin')
   






