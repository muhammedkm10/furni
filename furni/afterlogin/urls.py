from django.urls import path,include
from . import views

urlpatterns = [
    
    path('shop/',views.shop,name='shop'),
    path('productdetails/<str:id>/',views.product_details,name='productdetails'),
    path('showcart/',views.show_cart,name='showcart'),
    path('addtocart/<str:id>',views.add_to_cart,name='addtocart'),
    # path('updatecart/<str:id>/<int:op>',views.update_cart,name='uaddtocartpdatecart'),
    path('deletecart/<str:id>',views.delete_cart_product,name='deletecart'),
    path('wishlist/<str:id>',views.add_to_wishlist,name='wishlist'),
    path('showwishlist/',views.show_wish_list,name='showwishlist'),
    path('remove/<str:id>',views.delete_whish_list,name='remove'),
    path('updatequantity/',views.quantity_updation,name='updatequantity'),


    




    


]