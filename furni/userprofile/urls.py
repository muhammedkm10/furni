from django.urls import path,include
from . import views

urlpatterns = [
    
    path('userprofile/',views.show_user_profile,name='userprofile'),
    path('removeaddress/<str:id>',views.remove_address,name='removeaddress'),
    path('addaddressinuser/',views.add_address_in_user,name='addaddressinuser'),
    path('editaddressinuser/<str:id>',views.edit_address,name='editaddressinuser'),
    path('editprofile/<str:id>',views.edit_profile,name='editprofile'),
]