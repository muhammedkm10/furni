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
    path('salesreport/',views.sales_report,name='salesreport'),
    path('moredetailsinadmin/<str:id>',views.more_details_in_admin,name='moredetailsinadmin'),
    path('productoffer/',views.product_offers,name='productoffer'),
    path('categoryoffer/',views.category_offers,name='categoryoffer'),
    path('viewcategoryoffer/',views.view_category_offer,name='viewcategoryoffer'),
    path('viewproductoffer/',views.view_product_offer,name='viewproductoffer'),
    path('editproductoffer/<str:id>',views.edit_product_offer,name='editproductoffer'),
    path('editcategoryoffer/<str:id>',views.edit_category_offer,name='editcategoryoffer'),

    


    path('listcategoryoffer/<str:id>',views.list_category_offer,name='listcategoryoffer'),
    path('unlistcategoryoffer/<str:id>',views.un_list_category_offer,name='unlistcategoryoffer'),
    path('listproductoffer/<str:id>',views.list_product_offer,name='listproductoffer'),
    path('unlistproductoffer/<str:id>',views.un_list_product_offer,name='unlistproductoffer'),









]