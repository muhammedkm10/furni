from django.urls import path
from . import views

urlpatterns = [
    
    path('coupenmanage/',views.coupen_manage,name='coupenmanage'),
    path('addcoupon/',views.add_coupon,name='addcoupon'),
    path('editcoupon/<str:id>/',views.edit_coupon,name='editcoupon'),
    path('deletecoupon/<str:id>/',views.delete_coupon,name='deletecoupon'),
    path('listcoupen/<str:id>',views.list_coupen,name='listcoupen'),
    path('unlistcoupen/<str:id>',views.un_list_coupen,name='unlistcoupen'),



]