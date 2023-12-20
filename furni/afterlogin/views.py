from django.shortcuts import render
from product_manage.models import products

# Create your views here.




# shop
def shop(request):
    obj = products.objects.exclude(is_listed = False)
    context = {
        'items' : obj,
    }
    return render(request,'shop.html',context)

# product details
def product_details(request,id):
    obj = products.objects.get(id = id)
    context = {
        'items':obj
    }
    return render(request,'product_details.html',context)
