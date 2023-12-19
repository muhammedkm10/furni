from django.urls import path,include
from . import views

urlpatterns = [
    
    path('',views.index,name='index'),
    path('userlogin/',views.user_login,name='userlogin'),
    path('usersignup/',views.user_signup,name='usersignup'),
    path('otpverification/<str:id>/',views.otp_verification,name='otpverification'),
    path('logout/',views.logout,name='logout'),
    
]
