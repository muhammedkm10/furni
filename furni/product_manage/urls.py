from django.urls import path,include
from . import views

urlpatterns = [
    path('adminproductmanage/',views.product_manage,name='adminproductmanage'),
    path('editproduct/<str:id>',views.edit_product,name='editproduct'),
    path('addproduct/',views.add_product,name='addproduct'),
     path('deleteproduct/<str:id>',views.delete_product,name='deleteproduct'),
    
]

