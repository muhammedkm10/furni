from django.urls import path,include
from . import views

urlpatterns = [
    
    path('shop/',views.shop,name='shop'),
    path('productdetails/<str:id>/',views.product_details,name='productdetails'),
    
]