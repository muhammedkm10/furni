from django.shortcuts import render,HttpResponse,redirect
from product_manage.models import products
from logintohome.models import CustomUser1
from .models import cart
from django.db.models import Sum,Q
from category_management.models import category
from django.contrib import messages





# Create your views here.



# shop
def shop(request):
 
    obj = products.objects.filter(is_listed = True,category__is_listed = True )
    cat = category.objects.filter(is_listed = True)
    
    if 'email' in request.session:
            email  = request.session['email']
            user = CustomUser1.objects.get(email = email)
            id = user.id
            no_of_cart = cart.objects.filter(user_id = id).count()
    else: 
        no_of_cart = 0        
    context = {
        'items' : obj,
        'category':cat,
        'no':no_of_cart

    }
    return render(request,'shop.html',context)


# product details
def product_details(request,id):
    obj = products.objects.get(id = id)
    if 'email' in request.session:
            email  = request.session['email']
            user = CustomUser1.objects.get(email = email)
            id1 = user.id
            no_of_cart = cart.objects.filter(user_id = id1).count()
    else:
        no_of_cart = 0

    context = {
        'items':obj,
        'no':no_of_cart
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
    total_amount = cart.objects.filter(user_id=user.id).aggregate(sum = Sum('total'))
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
    cart1 = cart(user_id = user,product_id = obj,category = obj.category)
    cart1.save()
    messages.success(request,"Product added to cart successfully.......1")
    return redirect('productdetails',id)
   
    

# delete cart item
def delete_cart_product(request,id):
    cart.objects.get(id = id).delete()
    return redirect('showcart') 
    



# searching for category
def selection_for_category(request):
   if request.method == 'POST':
      try:
            cat1 = request.POST['catoo']
      except:
          cat1 = None
      obj = products.objects.filter(category__id = cat1)
      cat = category.objects.filter(is_listed = True)
      if 'email' in request.session:
            email  = request.session['email']
            user = CustomUser1.objects.get(email = email)
            id1 = user.id
            no_of_cart = cart.objects.filter(user_id = id1).count()
      else:
        no_of_cart = 0

      print(obj)
      context = {
                'items':obj,
                'category':cat,
                'no':no_of_cart


            }
      return render(request,'selected_category.html',context)
     




