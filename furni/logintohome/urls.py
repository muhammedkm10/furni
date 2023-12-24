from django.urls import path,include
from . import views

urlpatterns = [
    
    path('',views.index,name='index'),
    path('userlogin/',views.user_login,name='userlogin'),
    path('usersignup/',views.user_signup,name='usersignup'),
    path('otpverification/<str:id>/',views.otp_verification,name='otpverification'),
    path('logout/',views.logout,name='logout'),
    path('resetpassword/',views.reset_password,name='resetpassword'),
    path('resetpassotp/<str:otp>/<str:id>',views.reset_pass_otp,name='resetpassotp'),
    path('confirmpassword/<str:id>',views.confirm_password,name='confirmpassword'),
    path('aboutus/',views.about_us,name='aboutus'),
    path('contactus/',views.contact_us,name='contactus'),
    
]
