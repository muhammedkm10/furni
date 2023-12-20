from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache
from logintohome.models import CustomUser1
# Create your views here.

# admin login
@never_cache
def admin_login(request):
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



# admin home

@never_cache
def admin_home(request):
  if 'username' in request.session:
     return render(request,'admin_home.html')
  else:
    return redirect('adminlogin')

# admin  logout
@never_cache
def admin_logout(request):
  if 'username' in request.session:
    request.session.flush()
  return redirect('adminlogin')



# user manage

def user_manage(request):
  if 'username' in request.session:
    user = CustomUser1.objects.all()
    context = {
      'user':user
    }

    return render(request,'user_management.html',context)

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


