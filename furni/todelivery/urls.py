from django.urls import path,include
from . import views

urlpatterns = [
     path('proceedtocheckout/<int:last_added_address_id>/', views.proceed_to_checkout, name='proceedtocheckout'),
     path('addaddress/',views.add_address,name='addaddress'),
     path('orderconfirmation/',views.order_confirmation,name='orderconfirmation'),
     path('orderedbyrazor/',views.ordered_by_razor,name='orderedbyrazor'),
     path('thanks/',views.thanks,name='thanks'),

]