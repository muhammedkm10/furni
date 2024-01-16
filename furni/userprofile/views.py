from django.shortcuts import render,redirect
from logintohome.models import CustomUser1
from todelivery.models import address
from django.contrib import messages
import os
from django.views.decorators.cache import never_cache
from todelivery.models import ordered_items,order_details
from datetime import timedelta
from afterlogin.models import cart
from product_manage.models import products,variant
from .models import wallet
from django.db.models import Count
from datetime import datetime






# showing the details of user profile addresses user added and the other details
def show_user_profile(request):
    if 'email' in request.session:
     email1 = request.session['email']
     obj = CustomUser1.objects.get(email = email1)
     user = obj.id
     wal = wallet.objects.get(user_id = obj)
     no_of_cart = cart.objects.filter(user_id = user).count()
     addr = address.objects.filter(user_id = user,is_cancelled = False)
     context={
           'obj':obj,
           'addr':addr,
           'no':no_of_cart,
           'wal':wal

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
           if len(phone) == 10 and int(phone) > 0:
                if len(pin) == 6 and int(phone) > 0:
                    addobj = address(user_id = obj,first_name = fname,last_name=lname,address=addv,state=state,country=country,post=post,pin=pin,email=email,phone=phone)
                    addobj.save()
                    messages.success(request,"address added successfully")
                    return redirect('userprofile')
                else:
                    messages.success(request,"pin number should be valid")
                    return redirect('addaddressinuser')
           else:
               messages.success(request,"phone number should be valid")
               return redirect('addaddressinuser')
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
           obj.post  = post
           obj.email  = email
           if len(phone) == 10 and int(phone) > 0:
                if len(pin) == 6 and int(phone) > 0:
                        obj.phone  = phone
                        obj.pin  = pin
                        obj.save()
                        messages.success(request,"address edited successfully")
                        return redirect('userprofile')
                else:
                    messages.success(request,"pin number should be valid")
                    return redirect('editaddressinuser',id)
           else:
               messages.success(request,"phone number should be valid")
               return redirect('editaddressinuser',id)
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
        if image:
            if obj.profile:
                os.remove(obj.profile.path)
            obj.profile = image
        if len(phone) == 10 and int(phone) > 0:
            obj.phone = phone
            obj.save()
            messages.success(request,'profile updated successfully')
            return redirect('userprofile')
        else:
            messages.success(request,'phone number should valid')
            return redirect('editprofile')
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
    orders = order_details.objects.filter(user_id = user).order_by('-id')
    
    context = {
                'orders':orders,
               'no':no_of_cart
            }
    return render(request,'order_details.html',context)



#  cancel order
def cancel_order(request,id):
    email1 = request.session['email']
    user = CustomUser1.objects.get(email = email1)
    obj = ordered_items.objects.get(id= id)
    obj.status = 'cancelled'
    pro = variant.objects.get(product_id = obj.product_name,id = obj.size.id)
    pro.quantity = pro.quantity + obj.quantity
    obj.save()
    pro.save()
    if obj.order_id.pay_method == 'razor_pay' or obj.order_id.pay_method == 'wallet_pay' :
        if obj.order_id.coupen_applyed == True:
           wall = wallet.objects.get(user_id = user)
           print(obj.order_id.id)
           my_dict = ordered_items.objects.filter(order_id_id = obj.order_id.id).aggregate(no =  Count('id'))
           no_orders = my_dict['no']
           discount = obj.order_id.applied_coupen.cop_price
           print(discount)
           for_each_pro = int(discount/no_orders)
           rtrn_to_wlt = obj.total_amount - for_each_pro
           wall.amount = wall.amount + rtrn_to_wlt
           print(wall)
           wall.save()
           messages.success(request,"your order cacelled successfully")
           return redirect('orderdetails')
        else:
            wall = wallet.objects.get(user_id = user)
            wall.amount = wall.amount + obj.total_amount
            wall.save()
            messages.success(request,"your order cacelled successfully")
            return redirect('orderdetails')
    messages.success(request,"your order cacelled successfully")
    return redirect('orderdetails')





# track order 
def track_order(request,id):
    obj = ordered_items.objects.get(id = id)
    context = {
        'item' :obj
    }

    return render(request,'track.html',context)



# more details of the product
def more_details(request,id):
    obj = ordered_items.objects.filter(order_id_id = id)
    context = {
        'orders':obj,
    }
    return render(request,'more_details.html',context)



# invoice download
def invoice(request,id):
    obj = ordered_items.objects.get(order_id_id = id)
    current_date = datetime.now().date()
    print(current_date)
   
    context = {
        'item':obj,
        'date':current_date
    }
    return render(request,'invoice.html',context)



