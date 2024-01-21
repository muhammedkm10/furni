from django.contrib import admin
from .models import wallet,return_requests,product_review

# Register your models here.
admin.site.register(wallet)
admin.site.register(return_requests)
admin.site.register(product_review)
