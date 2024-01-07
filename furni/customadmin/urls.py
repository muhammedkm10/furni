from django.urls import path
from . import views

urlpatterns = [
    
    path('adminlogin/',views.admin_login,name='adminlogin'),
     path('adminhome/',views.admin_home,name='adminhome'),
    path('usermanage/',views.user_manage,name='usermanage'),
    path('adminlogout/',views.admin_logout,name='adminlogout'),
    path('blockuser/<str:id>',views.block_user,name='blockuser'),
    path('unblockuser/<str:id>',views.un_block_user,name='unblockuser'),
    path('searchuser/',views.search_for_user,name='searchuser'),
    path('ordersmanage/',views.order_management,name='ordersmanage'),
    path('editstatus/<str:id>',views.edit_status,name='editstatus'),
    path('cancelorder/<str:id>',views.cancel_order,name='cancelorder'),

]