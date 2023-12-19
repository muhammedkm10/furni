from django.shortcuts import render

# Create your views here.




# shop
def shop(request):
    return render(request,'shop.html')

# product details
def product_details(request):
    return render(request,'product_details.html')
