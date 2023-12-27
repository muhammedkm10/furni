from django.shortcuts import render,redirect
from logintohome.models import CustomUser1
from afterlogin.models import cart
from product_manage.models import products
from django.db.models import Sum
from django.views.decorators.cache import never_cache
from .models import address,order_details,ordered_items
from django.contrib import messages
from django.utils import timezone




# Create your views here.
@never_cache
def proceed_to_checkout(request):
    email1  =  request.session['email']
    obj = CustomUser1.objects.get(email = email1)
    userid = obj.id
    print(userid)
    cart_details = cart.objects.select_related('product_id').filter(user_id = userid)
    total = cart.objects.filter(user_id = userid).aggregate(sum = Sum('total'))
    addresses = address.objects.filter(user_id=userid)
    context = {
    
        'cart_details': cart_details,
        'total':total,
        'addresses':addresses
    }
    print(context)

    return render(request,'proceed_to_checkout.html',context)


# add address
def add_address(request):
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
           return redirect('proceedtocheckout')
     return render(request,'add_address.html')



# after clicking place order order confirmation view
# this view will save the data in two table it save the order details and the order item details in another related table
def order_confirmation(request):
       if request.method == "POST":
           email1  =  request.session['email']
           obj = CustomUser1.objects.get(email = email1)
           userid = obj.id
           paymethod = request.POST['paymethod']
           orderdate = timezone.now().date()
           addres = request.POST['address']
           ad = address.objects.get(id = addres)
           ad1 = ad.id
           order = order_details(user_id = obj,pay_method = paymethod, order_date = orderdate,addres = ad1)
           order.save()
           cart_items  = cart.objects.filter(user_id = userid)
           for i in cart_items:
                item = ordered_items(order_id = order,product_name = i.product_id.name,quantity=i.quantity,total_amount = i.total,status = "ordered" ,category= i.category)
                item.save()
                i.delete()
           return render(request,'thank_you.html')


     
     


