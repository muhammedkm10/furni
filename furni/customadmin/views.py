from django.shortcuts import render

# Create your views here.

# admin login
def admin_login(request):
  return render(request,'admin_login.html')

# user manage
def user_manage(request):
  return render(request,'user_management.html')


# admin home
def admin_home(request):
  return render(request,'admin_home.html')