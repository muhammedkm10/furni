from django.urls import path,include
from . import views

urlpatterns = [
    path('proceedtocheckout/',views.proceed_to_checkout,name='proceedtocheckout'),
     path('addaddress/',views.add_address,name='addaddress'),
     path('orderconfirmation/',views.order_confirmation,name='orderconfirmation'),

]