from django.shortcuts import render,redirect
from logintohome.models import CustomUser1
from afterlogin.models import cart
from product_manage.models import products
from django.db.models import Sum
from django.views.decorators.cache import never_cache
from .models import address,order_details,ordered_items,proceedtocheckout
from django.contrib import messages
from django.utils import timezone
from datetime import  timedelta
from django.http import JsonResponse
from django.urls import reverse
from userprofile.models import wallet
from coupenapp.models import coupons
from django.utils import timezone
from datetime import datetime
from django.urls import reverse
from django.http import JsonResponse




# Create your views here.
@never_cache
def proceed_to_checkout(request, last_added_address_id):
    email1  =  request.session['email']
    obj = CustomUser1.objects.get(email = email1)
    userid = obj.id
    wal = wallet.objects.get(user_id = userid)
    walamount = wal.amount
    orderdate = timezone.now().date()
    if last_added_address_id == None:
        messages.error(request,'add some address here')
        return redirect('userprofile')
    cart_details = cart.objects.select_related('product_id').filter(user_id = userid).order_by('-id')
    # if cart_details.product_id.quantity < cart_details.quantity:
    try:
        no = cart.objects.filter(user_id = obj).count()
    except:
        no = 0
            
    if cart_details.exists():
            total1 = cart.objects.filter(user_id = userid).aggregate(sum = Sum('total'))
            total_amount = total1['sum']
            addresses = address.objects.filter(user_id = userid,is_cancelled = False)
            proceedtocheckout.objects.create(user_id  = obj,order_date = orderdate,total_amount = total_amount,discount_amount = total_amount)
            try:
              details = proceedtocheckout.objects.get(user_id  = obj)
            except:
                  proceedtocheckout.objects.filter(user_id  = obj).delete()
                  proceedtocheckout.objects.create(user_id  = obj,order_date = orderdate,total_amount = total_amount,discount_amount = total_amount)
                  details = proceedtocheckout.objects.get(user_id  = obj)
                 
            context = {
                'details':details,
                'cart_details': cart_details,
                'total1':total1,
                'addresses':addresses,
                'last_added_address_id': last_added_address_id,
                'user' :obj,
                'wal':walamount,
                'no':no
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


# payment using cod
# after clicking place order order confirmation view
# this view will save the data in two table it save the order details and the order item details in another related table
def order_confirmation(request):
       if request.method == "POST":
           email1  =  request.session['email']
           obj = CustomUser1.objects.get(email = email1)
           userid = obj.id
           checkout = proceedtocheckout.objects.get(user_id = obj)
           orderdate = timezone.now().date()
           addres = request.POST['address']
           ad = address.objects.get(id = addres)
           ad1 = ad.id
           order = order_details(user_id = obj,pay_method = "cod", order_date = orderdate,addres = ad,total_amount = checkout.total_amount,applied_coupen = checkout.applyed_coupen,coupen_applyed = checkout.coupen_applyed,after_discount = checkout.discount_amount)
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
           checkout.delete()
           return render(request,'thank_you.html')

# order by razor pay
def ordered_by_razor(request) :
      if request.method == 'POST':
           email1  =  request.session['email']
           obj = CustomUser1.objects.get(email = email1)
           userid = obj.id
           orderdate = timezone.now().date()
           checkout = proceedtocheckout.objects.get(user_id = obj)
           i = request.POST.get('address_id')
           ad = address.objects.get(id = i)
           ad1 = ad.id
           order = order_details(user_id = obj,pay_method = "razor_pay", order_date = orderdate,addres = ad,total_amount = checkout.total_amount,applied_coupen = checkout.applyed_coupen,coupen_applyed = checkout.coupen_applyed,after_discount = checkout.discount_amount)
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
           checkout.delete()
           response_data = {
           'success': True,
           'redirect_url': reverse('thanks')
             }
           return JsonResponse(response_data)



# order by the wallet
def pay_using_wallet(request):
     if request.method == 'POST':
           email1  =  request.session['email']
           obj = CustomUser1.objects.get(email = email1)
           userid = obj.id  
           checkout = proceedtocheckout.objects.get(user_id = obj)
           total = int(request.POST['total2'])
           i = request.POST.get('address_id')
           orderdate = timezone.now().date()
           print('hai',total)
           wal = wallet.objects.get(user_id = userid)
           wlt_amnt = wal.amount
           if total <= wlt_amnt:
                ad = address.objects.get(id = i)
                ad1 = ad.id
                order = order_details(user_id = obj,pay_method = "wallet_pay", order_date = orderdate,addres = ad,total_amount = checkout.total_amount,applied_coupen = checkout.applyed_coupen,coupen_applyed = checkout.coupen_applyed,after_discount = checkout.discount_amount)
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
                checkout.delete()
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


# apply coupon 
def apply_coupon(request):
    ad = address.objects.last()
    email1  =  request.session['email']
    user = CustomUser1.objects.get(email = email1)
    userid = user.id  
    if request.method == 'POST':
        coupon = request.POST['coupon']
        orders = order_details.objects.filter(user_id_id = user.id)
        d = timezone.now().date()
        try:
            obj = coupons.objects.get(code = coupon)
        except coupons.DoesNotExist:
            return JsonResponse({'error': 'There is no coupon to apply'})
        if obj is not None:
            detail = proceedtocheckout.objects.get(user_id = userid)
            date1 = obj.from_date
            date2 = obj.to
            copdate = d
            p = []
            for i in orders:
                if i.applied_coupen and i.applied_coupen.id is not None:
                    p.append(i.applied_coupen.id)
            print(p)
            print(obj.id)
            if  obj.id not in p:
                            if coupon == obj.code and copdate < date2 and copdate >= date1:
                                        detail.discount_amount  = detail.total_amount - obj.cop_price
                                        if detail.discount_amount  < 0:
                                            detail.discount_amount = 0
                                            detail.applyed_coupen = obj
                                            detail.coupen_applyed = True
                                            detail.save()
                                        detail.applyed_coupen = obj
                                        detail.coupen_applyed = True
                                        print("amount",detail.discount_amount)
                                        detail.save()
                                        return JsonResponse({'success': 'Coupon applied successfully to cancel the coupon press cancel button', 'updatedTotal': detail.discount_amount})
                            else:
                                        return JsonResponse({'error': 'invalid Coupon'})
            else:
                        return JsonResponse({'error': 'coupen is already applied..'})
            
    return JsonResponse({'error': 'Invalid request'})



# thanks .html
def thanks(request):
      return render(request,'thank_you.html')
# sorry .html
def sorry(request):
      return render(request,'sorry.html')
