from django.shortcuts import render,redirect
from logintohome.models import CustomUser1
from todelivery.models import address
from django.contrib import messages
import os
from django.views.decorators.cache import never_cache
from todelivery.models import ordered_items,order_details
from datetime import timedelta
from afterlogin.models import cart



# Create your views here.



# showing the details of user profile addresses user added and the other details
def show_user_profile(request):
    if 'email' in request.session:
     email1 = request.session['email']
     obj = CustomUser1.objects.get(email = email1)
     user = obj.id
     no_of_cart = cart.objects.filter(user_id = user).count()
     addr = address.objects.filter(user_id = user,is_cancelled = False)
     context={
           'obj':obj,
           'addr':addr,
           'no':no_of_cart
     }
     return render(request,'user_profile.html',context)
    return render(request, '404.html', status=404)



# removing the addresses user added
def remove_address(request,id):
    add = address.objects.get(id = id)
    print(add)
    print(add.user_id.id)
    add.is_cancelled = True
    add.save()
    return redirect('userprofile')
   

# adding new address
def add_address_in_user(request):
     if request.method == "POST":
           email1  =  request.session['email']
           obj = CustomUser1.objects.get(email = email1)
           fname = request.POST['fname']
           lname = request.POST['lname']
           addv = request.POST['address']
           state = request.POST['state']
           country = request.POST['country']
           post = request.POST['post']
           pin = request.POST['pin']
           email = request.POST['email']
           phone = request.POST['phone']
           addobj = address(user_id = obj,first_name = fname,last_name=lname,address=addv,state=state,country=country,post=post,pin=pin,email=email,phone=phone)
           addobj.save()
           messages.success(request,"address added successfully")
           return redirect('userprofile')
     return render(request,'add_address_in_user.html')
   

# edit address

def edit_address(request,id):
    obj = address.objects.get(id = id)
    context = {
            'obj':obj,
        }
    if request.method == 'POST':
           
           fname = request.POST['fname']
           lname = request.POST['lname']
           addv = request.POST['address']
           state = request.POST['state']
           country = request.POST['country']
           post = request.POST['post']
           pin = request.POST['pin']
           email = request.POST['email']
           phone = request.POST['phone']
           obj.first_name  = fname
           obj.last_name  = lname
           obj.address  = addv
           obj.state  = state
           obj.country  = country
           obj.pin  = pin
           obj.post  = post
           obj.email  = email
           obj.phone  = phone
           obj.save()
           messages.success(request,"address edited successfully")
           return redirect('userprofile')
    return render(request,'edit_address.html',context)




# edit profile
def edit_profile(request): 
    email1 = request.session['email']
    obj = CustomUser1.objects.get(email = email1)
    context = {
        'user':obj,
    }
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        image = request.FILES['editprofile'] if request.FILES else None
        obj.username = name
        obj.phone = phone
        if image:
            if obj.profile:
                os.remove(obj.profile.path)
            obj.profile = image
        obj.save()
        messages.success(request,'profile updated successfully')
        return redirect('userprofile')
    return render(request,'edit_userprofile.html',context)




# change password
@never_cache
def change_password(request):
    email1 = request.session['email']
    obj = CustomUser1.objects.get(email = email1)
    oldpass = obj.password 
    if request.method == "POST":
        entered = request.POST['pass']
        if entered == oldpass:
           return redirect('confirming')
        messages.error(request,'enter a valid password')
        return redirect('changepassword')
    return render(request,'old_password.html')



# confirmation of password and setting new password
@never_cache
def cofirmation(request):
    email1 = request.session['email']
    obj = CustomUser1.objects.get(email = email1)
    if request.method == 'POST':
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1 == pass2:
            obj.password = pass1
            obj.save()
            messages.success(request,'your password changed successfully...!')
            return redirect('userprofile')
        messages.error(request,'the passwords should be same')
    return render(request,'change_password.html')




# order details
def orderdetails(request):
    email1 = request.session['email']
    obj = CustomUser1.objects.get(email = email1)
    user = obj.id
    no_of_cart = cart.objects.filter(user_id = user).count()
    orders = ordered_items.objects.filter(user = user).order_by('-id')

    context = {
                'orders':orders,
               'no':no_of_cart
            }
    return render(request,'order_details.html',context)



#  cancel order
def cancel_order(request,id):
    obj = ordered_items.objects.get(id= id)
    obj.status = 'cancelled'
    obj.save()
    messages.success(request,"your order cacelled successfully")
    return redirect('orderdetails')




# track order 
def track_order(request,id):
    obj = ordered_items.objects.get(id = id)
    context = {
        'item' :obj
    }

    return render(request,'track.html',context)

