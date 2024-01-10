from django.shortcuts import render,HttpResponse,redirect
from product_manage.models import products,variant
from logintohome.models import CustomUser1
from .models import cart,wishlist
from django.db.models import Sum,Q
from category_management.models import category
from django.contrib import messages
from django.core.paginator import Paginator
from todelivery.models import address
from django.http import JsonResponse






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
    variants = variant.objects.all()
    if 'email' in request.session:
            email  = request.session['email']
            user = CustomUser1.objects.get(email = email)
            id1 = user.id
            no_of_cart = cart.objects.filter(user_id = id1).count()
    else:
        no_of_cart = 0

    context = {
        'items':obj,
        'no':no_of_cart,
        'variant':variants
    }
    return render(request,'product_details.html',context)


# user cart
def show_cart(request):
    email1 = request.session['email']
    user = CustomUser1.objects.get(email = email1)
    item  =  cart.objects.select_related('product_id').filter(user_id = user).order_by('-id')
    for i in item:
      i.total = i.product_id.price*i.quantity
      i.save()
    total_amount = cart.objects.filter(user_id=user.id).aggregate(sum = Sum('total'))
    last_added_address = address.objects.filter(user_id=user).order_by('-id').first()
    print(last_added_address)
    if last_added_address == None:
        messages.error(request,'add some address here')
        return redirect('userprofile')
    last_added_address_id = last_added_address.id
    
    context = {
      'item':item,
      'total_amount':total_amount,
      'last_added_address_id' : last_added_address_id
 
    }
    
    return render(request,'cart.html',context)


# quantity updation
def quantity_updation(request):
    print('hai')
    if request.method =='POST':
        cart_id = int(request.POST['cart_id'])
        print('cart',cart_id)
        action =  request.POST['action']
        obj = cart.objects.get(id = cart_id)
        print(obj.product_id)
        print(obj.size.id)
        pro = products.objects.get(name = obj.product_id)
        print(pro)
        size_qnty = variant.objects.get(product_id__name = pro,id = obj.size.id)
        print(size_qnty.id)
        print(size_qnty.quantity)
        if action == 'plus':
            if obj.quantity < 5 and obj.quantity < size_qnty.quantity:
                obj.quantity += 1
                obj.save()
            else:
                obj.quantity = 5

        else:
           if obj.quantity > 1: 
                obj.quantity -=1
                obj.save()
           else:
               obj.quantity = 0
        return JsonResponse({'status':'alsjdjhfp'})

    


# add to cart
def add_to_cart(request,id):
    if request.method == 'POST':
        try:
         size = request.POST['size']
        except:
            size = None
        if size != None:
            obj = variant.objects.get(product_id = id,size = size)
            pro = products.objects.get(id = id)
            email1 = request.session['email']
            print(size)
            try:
             quantity = int(request.POST['qnty'])
            except:
                quantity = None
            
            if quantity > 0:
                if quantity < 6 :
                        if obj.quantity >= quantity:
                                user = CustomUser1.objects.get(email = email1)
                                if cart.objects.filter(product_id = pro,size_id = obj.id).exists():
                                    messages.success(request,"Product is already in cart")
                                    return redirect('showcart')
                                else:
                                        cart1 = cart(user_id = user,product_id = pro,category = pro.category,quantity = quantity,size = obj)
                                        cart1.save()
                                        messages.success(request,"Product added to cart successfully.......")
                                        return redirect('showcart')
                        else:
                            messages.success(request,"Sorry.......product is out of stock....")
                            path1 = request.GET.get('next')
                            return redirect(path1,id)
                else:
                    messages.success(request,"quantity should be less than or equal to 5...")
                    path1 = request.GET.get('next')
                    return redirect(path1,id)
            else:
                messages.success(request,"quantity should be greater than or equal to 1...")
                path1 = request.GET.get('next')
                return redirect(path1,id)
        else:
            messages.success(request,"the product is out of stock")
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
    size = request.POST['size']
    var = variant.objects.get(size = size,product_id_id = id)
    print(size)
    pro = products.objects.get(id = id)
    if wishlist.objects.filter(product_id = pro,size__id = var.id ).exists():
        messages.success(request,"Product is already in wishlist")
        return redirect('showwishlist')
    else:
        obj = wishlist(user_id = user,product_id = pro,size = var)
        obj.save()
        messages.success(request,"Product added to wishlist successfully.......")
        return redirect('productdetails',id)




# wishlist item into cart
def whishtocart(request,pro_id,w_id):
    email = request.session['email']
    user = CustomUser1.objects.get(email = email)
    pro = products.objects.get(id = pro_id)
    whish_item = wishlist.objects.get(id = w_id)
    var = variant.objects.get(product_id_id = pro.id,id = whish_item.size.id)
    if var.quantity >= 1:
        if cart.objects.filter(product_id = pro,size = var).exists():
                messages.success(request,"Product is already in cart")
                return redirect('showcart')
        obj = cart(user_id = user,product_id = pro,quantity = 1,category = pro.category,size  =  var) 
        wishlist.objects.get(product_id = pro,size = var).delete()
        obj.save()
        
        messages.success(request,"Product added to cart successfully.......")
        return redirect('showcart')
    else:
         messages.error(request,"Product is out of stock")
         return redirect('showwishlist')
    


# show whishlist
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
    


