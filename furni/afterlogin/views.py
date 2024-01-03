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
 
    obj = products.objects.filter(is_listed = True,category__is_listed = True )
    cat = category.objects.filter(is_listed = True)
    paginator = Paginator(obj, 12)  # 10 products per page
    page_number = request.GET.get('page')  # Get the current page number from the request query parameters
    page_obj = paginator.get_page(page_number)
    
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
        'no':no_of_cart,
        'page_obj': page_obj

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
    



# searching for category
def selection_for_category(request):
   if request.method == 'POST':
      try:
            cat1 = request.POST['catoo']
            min = int(request.POST['min'])
            max = int(request.POST['max'])  
            sort = request.POST['sort']  
      except:
          cat1 = None
      if max > min:
                if sort == 'asc':
                   obj = products.objects.filter(category__id = cat1,price__range=(min,max)).order_by('price')
                else:
                    obj = products.objects.filter(category__id = cat1,price__range=(min,max)).order_by('-price')
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
      messages.error(request,"please enter a valid price range")
      return redirect('shop') 
     



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
    


