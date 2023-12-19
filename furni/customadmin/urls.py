from django.urls import path
from . import views

urlpatterns = [
    
    path('adminlogin/',views.admin_login,name='adminlogin'),
     path('adminhome/',views.admin_home,name='adminhome'),
    path('usermanage/',views.user_manage,name='usermanage'),
]