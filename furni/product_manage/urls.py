from django.urls import path,include
from . import views

urlpatterns = [
    path('adminproductmanage/',views.product_manage,name='adminproductmanage'),
    path('editproduct/<str:id>',views.edit_product,name='editproduct'),
    path('addproduct/',views.add_product,name='addproduct'),
     path('searchforproduct/',views.search_product,name='searchforproduct'),
     path('listproduct/<str:id>/',views.list_product,name='listproduct'),
     path('unlistproduct/<str:id>/',views.un_list_product,name='unlistproduct'),
    
]

