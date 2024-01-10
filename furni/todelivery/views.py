from django.shortcuts import render,redirect
from logintohome.models import CustomUser1
from afterlogin.models import cart
from product_manage.models import products
from django.db.models import Sum
from django.views.decorators.cache import never_cache
from .models import address,order_details,ordered_items
from django.contrib import messages
from django.utils import timezone
from datetime import  timedelta
from django.http import JsonResponse
from django.urls import reverse
from userprofile.models import wallet





# Create your views here.
@never_cache
def proceed_to_checkout(request, last_added_address_id):
    email1  =  request.session['email']
    obj = CustomUser1.objects.get(email = email1)
    userid = obj.id
    wal = wallet.objects.get(user_id = userid)
    walamount = wal.amount
    
    if last_added_address_id == None:
        messages.error(request,'add some address here')
        return redirect('userprofile')
    cart_details = cart.objects.select_related('product_id').filter(user_id = userid).order_by('-id')
    # if cart_details.product_id.quantity < cart_details.quantity:
    if cart_details.exists():
            total = cart.objects.filter(user_id = userid).aggregate(sum = Sum('total'))
            addresses = address.objects.filter(user_id = userid,is_cancelled = False)
            context = {
            
                'cart_details': cart_details,
                'total':total,
                'addresses':addresses,
                'last_added_address_id': last_added_address_id,
                'user' :obj,
                'wal':walamount,
            }
            
        

            return render(request,'proceed_to_checkout.html',context)
    else:
            messages.error(request,"add some products")
            return redirect('showcart')
    
  
         



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
           if len(phone) == 10 and int(phone) > 0:
                if len(pin) == 6 and int(phone) > 0:
                    addobj = address(user_id = obj,first_name = fname,last_name=lname,address=addv,state=state,country=country,post=post,pin=pin,email=email,phone=phone)
                    addobj.save()
                    last_added_address_id = addobj.id
                    messages.success(request,"address added successfully")
                    return redirect('proceedtocheckout', last_added_address_id = last_added_address_id)
                else:
                    messages.success(request,"pin number should be valid")
                    return redirect('addaddressinuser')
           else:
               messages.success(request,"phone number should be valid")
               return redirect('addaddressinuser')
     return render(request,'add_address.html')



# after clicking place order order confirmation view
# this view will save the data in two table it save the order details and the order item details in another related table
def order_confirmation(request):
       if request.method == "POST":
           email1  =  request.session['email']
           obj = CustomUser1.objects.get(email = email1)
           userid = obj.id
           orderdate = timezone.now().date()
           addres = request.POST['address']
           ad = address.objects.get(id = addres)
           ad1 = ad.id
           order = order_details(user_id = obj,pay_method = "cod", order_date = orderdate,addres = ad1)
           order.save()
           cart_items  = cart.objects.filter(user_id = userid)
           for i in cart_items:
                item = ordered_items(order_id = order,product_name = i.product_id,quantity = i.quantity,total_amount = i.total,status = "ordered" ,category= i.category,user = order.user_id.id,add = ad,expected  = orderdate + timedelta(days=7),size = i.size)
                item.save()
                print(item.size.quantity)
                item.size.quantity = item.size.quantity-item.quantity
                item.size.save()
                print(item.size.quantity)
                i.delete()
           return render(request,'thank_you.html')

# order by razor pay
def ordered_by_razor(request) :
      if request.method == 'POST':
           email1  =  request.session['email']
           obj = CustomUser1.objects.get(email = email1)
           userid = obj.id
           orderdate = timezone.now().date()
           i = request.POST.get('address_id')
           ad = address.objects.get(id = i)
           ad1 = ad.id
           order = order_details(user_id = obj,pay_method = "razor_pay", order_date = orderdate,addres = ad1)
           order.save()
           cart_items  = cart.objects.filter(user_id = userid)
           for i in cart_items:
                item = ordered_items(order_id = order,product_name = i.product_id,quantity = i.quantity,total_amount = i.total,status = "ordered" ,category= i.category,user = order.user_id.id,add = ad,expected  = orderdate + timedelta(days=7),size = i.size)
                item.save()
                print(item.size.quantity)
                item.size.quantity = item.size.quantity-item.quantity
                item.size.save()
                print(item.size.quantity)
                i.delete()
           response_data = {
           'success': True,
           'redirect_url': reverse('thanks')
             }
           return JsonResponse(response_data)



# order by the walle
def pay_using_wallet(request):
     if request.method == 'POST':
           email1  =  request.session['email']
           obj = CustomUser1.objects.get(email = email1)
           userid = obj.id  
           total = int(request.POST['total'])
           i = request.POST.get('address_id')
           orderdate = timezone.now().date()
           print(total)
           wal = wallet.objects.get(user_id = userid)
           wlt_amnt = wal.amount
           if total <= wlt_amnt:
                ad = address.objects.get(id = i)
                ad1 = ad.id
                order = order_details(user_id = obj,pay_method = "wallet_pay", order_date = orderdate,addres = ad1)
                order.save()
                cart_items  = cart.objects.filter(user_id = userid)
                for i in cart_items:
                        item = ordered_items(order_id = order,product_name = i.product_id,quantity = i.quantity,total_amount = i.total,status = "ordered" ,category= i.category,user = order.user_id.id,add = ad,expected  = orderdate + timedelta(days=7),size = i.size)
                        item.save()
                        print(item.size.quantity)
                        item.size.quantity = item.size.quantity-item.quantity
                        item.size.save()
                        print(item.size.quantity)
                        i.delete()
                wal.amount = wal.amount - total
                wal.save()
                response_data = {
                            'success': True,
                            'redirect_url': reverse('thanks')
                        }
                return JsonResponse(response_data)
           else:
                response_data = {
                            'success': True,
                            'redirect_url': reverse('sorry')
                        }
                return JsonResponse(response_data)
    

# thanks .html
def thanks(request):
      return render(request,'thank_you.html')
# sorry .html
def sorry(request):
      return render(request,'sorry.html')
