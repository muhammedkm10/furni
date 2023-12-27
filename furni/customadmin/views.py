from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache
from logintohome.models import CustomUser1
from todelivery.models import order_details,ordered_items,address
from product_manage.models import products
from django.http import HttpResponseServerError


# Create your views here.

# admin login
@never_cache
def admin_login(request):
  if 'email' not in request.session:
    if 'username' in request.session:
      return redirect('adminhome')
    if request.method == 'POST':
      username = request.POST['name']
      password = request.POST['pass']
      obj = authenticate(username = username,password  = password)
      if obj is not None:
        request.session['username'] =  username
        messages.success(request,"you are welcome.....!")
        return redirect('adminhome')
      else:
        messages.error(request,"enter a valid username or password")
        return redirect('adminlogin')
    return render(request,'admin_login.html')
  else:
     return render(request, '404.html', status=404)



# admin home

@never_cache
def admin_home(request):
  if 'email' not in request.session:
    if 'username' in request.session:
      return render(request,'admin_home.html')
    else:
      return redirect('adminlogin')
  else:
     return render(request, '404.html', status=404)

# admin  logout
@never_cache
def admin_logout(request):
  if 'username' in request.session:
    request.session.flush()
  return redirect('adminlogin')



# user manage

def user_manage(request):
  if 'email' not in request.session:
    if 'username' in request.session:
      user = CustomUser1.objects.all()
      context = {
        'user':user
      }

      return render(request,'user_management.html',context)
  else:
     return render(request, '404.html', status=404)

# block user

def block_user(request,id):
   if 'username' in request.session:
    obj = CustomUser1.objects.get(id = id)
    obj.is_blocked = True
    obj.save()
    return redirect('usermanage')

# un block user

def un_block_user(request,id):
   if 'username' in request.session:
    obj = CustomUser1.objects.get(id = id)
    obj.is_blocked = False
    obj.save()
    return redirect('usermanage')


# search for user

def search_for_user(request):
  if 'username' in request.session:
        if request.method == 'POST':
            query = request.POST['query']
            user = CustomUser1.objects.filter(username__icontains = query)
            context = {
              'user':user,
            }
        return render(request,'user_management.html',context)




# order management
  
def order_management(request): 
        if 'email' not in request.session:
          if 'username' in request.session:
                  obj = ordered_items.objects.select_related('order_id')
                  context = {
                            'items':obj,
                            
                          }
                  return render(request,'order_management.html',context)
          else:
             return redirect('adminlogin')
        else:
          return render(request, '404.html', status=404)
    





# edit status
def edit_status(request,id):
     if request.method == 'POST':
       changestatus = request.POST['changestatus']
       obj = ordered_items.objects.get(id = id)
       obj.status = changestatus
       obj.save()       
     return redirect('ordersmanage')


# cancel order
def cancel_order(request,id):
  obj = ordered_items.objects.get(id = id)
  obj.status = "cancelled by admin"
  obj.save()
  return redirect('ordersmanage')


