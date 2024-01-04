from django.shortcuts import render,HttpResponse,redirect
from product_manage.models import products
from logintohome.models import CustomUser1
from .models import cart,wishlist
from django.db.models import Sum,Q
from category_management.models import category
from django.contrib import messages
from django.core.paginator import Paginator
from todelivery.models import address





# Create your views here.



# shop
def shop(request):
    data = request.GET.get('data')
    price1 = request.GET.get('price1')
    sort = request.GET.get('sort')
    print(sort)

    obj = products.objects.filter(is_listed = True,category__is_listed = True )
  
    if data == "all":
        obj = products.objects.filter(is_listed = True,category__is_listed = True )
    if data == "seating_furniture":
        obj = products.objects.filter(category = 7,is_listed = True,category__is_listed = True )
    if data == "sleaping_furniture":
        obj = products.objects.filter(category = 8,is_listed = True,category__is_listed = True )
    if data == "tables":
        obj = products.objects.filter(category = 10,is_listed = True,category__is_listed = True )
    if data == "storage_furniture":
        obj = products.objects.filter(category = 12,is_listed = True,category__is_listed = True )
    if sort == "asc":
        obj = products.objects.filter(is_listed = True,category__is_listed = True ).order_by('price')
    if sort == "desc":
        obj = products.objects.filter(is_listed = True,category__is_listed = True ).order_by('-price')
    if price1 == "o":
        obj = products.objects.filter(price__range = (0,100),is_listed = True,category__is_listed = True )
    if price1 == "a":
        obj = products.objects.filter(price__range = (100,500),is_listed = True,category__is_listed = True )
    if price1 == "b":
        obj = products.objects.filter(price__range = (500,1500),category = 7,is_listed = True,category__is_listed = True )
    if price1 == "c":
        obj = products.objects.filter(price__range = (1500,2500),category = 8,is_listed = True,category__is_listed = True )
    if price1 == "d":
        obj = products.objects.filter(price__range = (2500,5000),category = 10,is_listed = True,category__is_listed = True )
    if price1 == "e":
        obj = products.objects.filter(price__range = (5000,7000),category = 12,is_listed = True,category__is_listed = True )
    if price1 == "f":
        obj = products.objects.filter(price__range = (7000,15000),category = 12,is_listed = True,category__is_listed = True )
    cat = category.objects.filter(is_listed = True)   
    if 'email' in request.session:
            email  = request.session['email']
            user = CustomUser1.objects.get(email = email)
            id = user.id
            no_of_cart = cart.objects.filter(user_id = id).count()
    else: 
        no_of_cart = 0     
    paginator = Paginator(obj, 8)  # 10 products per page
    page_number = request.GET.get('page')  # Get the current page number from the request query parameters
    page_obj = paginator.get_page(page_number)   
    context = {
    'items': obj,
    'category': cat,
    'no': no_of_cart,
    'page_obj': page_obj,
    'data': data,  # Pass the 'data' filter parameter to the context
    'price1': price1,  # Pass the 'price1' filter parameter to the context
    'sort':sort
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
    last_added_address = address.objects.filter(user_id=user).order_by('-id').first()
    print(last_added_address)
    last_added_address_id = last_added_address.id
    context = {
      'item':item,
      'total_amount':total_amount,
      'last_added_address_id' : last_added_address_id
 
    }
    
    return render(request,'cart.html',context)


# update cart 
def update_cart(request, id,op):
   
    cart_item = cart.objects.get(id=id)
   
    if op == 0:
      if cart_item.quantity < 5:
        if cart_item.product_id.quantity > cart_item.quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.success(request,"Product is out of stock")
            return redirect('showcart')
      else:
         cart_item.quantity = 5
         cart_item.save()
    else:
        if cart_item.quantity > 1:
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
    if cart.objects.filter(product_id = obj).exists():
        messages.success(request,"Product is already in cart")
        return redirect('showcart')
    cart1 = cart(user_id = user,product_id = obj,category = obj.category)
    cart1.save()
    messages.success(request,"Product added to cart successfully.......1")
    path1 = request.GET.get('next')
    return redirect(path1,id)
   
    



# delete cart item
def delete_cart_product(request,id):
    cart.objects.get(id = id).delete()
    return redirect('showcart') 
    



# add products to wish list
def add_to_wishlist(request,id):
    email = request.session['email']
    user =  CustomUser1.objects.get(email = email )
    pro = products.objects.get(id = id)
    if wishlist.objects.filter(product_id = pro).exists():
        messages.success(request,"Product is already in wishlist")
        return redirect('showwishlist')
    else:
        obj = wishlist(user_id = user,product_id = pro)
        obj.save()
        messages.success(request,"Product added to wishlist successfully.......")
        return redirect('productdetails',id)


# show cart
def show_wish_list(request):
    email = request.session['email']
    user = CustomUser1.objects.get(email = email)
    user_id = user.id
    pros = wishlist.objects.filter(user_id = user_id)
    context = {
        'items' : pros
    }
    return render(request,'wishlist.html',context)



# remove from wishlist
def delete_whish_list(request,id):
    wishlist.objects.get(id = id).delete()
    return redirect('showwishlist') 
    


