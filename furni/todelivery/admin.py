from django.contrib import admin
from .models import address,order_details,ordered_items,proceedtocheckout

# Register your models here.
admin.site.register(address)
admin.site.register(order_details)
admin.site.register(ordered_items)
admin.site.register(proceedtocheckout)



