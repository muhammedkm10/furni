from django.shortcuts import render,HttpResponse,redirect
from product_manage.models import products
from logintohome.models import CustomUser1
from .models import cart
from django.db.models import Sum




# Create your views here.




# shop
def shop(request):
    obj = products.objects.exclude(is_listed = False)
    context = {
        'items' : obj,
    }
    return render(request,'shop.html',context)

# product details
def product_details(request,id):
    obj = products.objects.get(id = id)
    context = {
        'items':obj
    }
    return render(request,'product_details.html',context)


# user cart
def show_cart(request):
    email1 = request.session['email']
    user = CustomUser1.objects.get(email = email1)
    item  =  cart.objects.select_related('product_id').filter(user_id = user)
    for i in item:
      i.total = i.product_id.price*i.quantity
      i.save()
    total_amount = cart.objects.aggregate(sum = Sum('total'))
    print(total_amount)
    
    context = {
      'item':item,
      'total_amount':total_amount,
 
    }

    return render(request,'cart.html',context)


# update cart 
def update_cart(request, id,op):
   
    cart_item = cart.objects.get(id=id)
   
    if op == 0:
      if cart_item.quantity <5:
        cart_item.quantity += 1
        cart_item.save()
      else:
         cart_item.quantity = 5
         cart_item.save()
    else:
        if cart_item.quantity >1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
           cart_item.quantity = 1
           cart_item.save()
        
    return redirect('showcart') 
    

    


# add to cart
def add_to_cart(request,id):
    obj = products.objects.get(id = id)
    email1 = request.session['email']
    user = CustomUser1.objects.get(email = email1)
    cart1 = cart(user_id = user,product_id = obj)
    cart1.save()
    return redirect('productdetails',id)
   
    

# delete cart item
def delete_cart_product(request,id):
    cart.objects.get(id = id).delete()
    return redirect('showcart') 
    







