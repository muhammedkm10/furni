from django.shortcuts import render,redirect
from . models import products
from category_management import models
from django.contrib import messages
import os
# Create your views here.
def product_manage(request):
    obj = products.objects.select_related('category').all()
    context = {
        'items':obj
    }
    return render(request,'product.html',context)


# edit product
def edit_product(request,id):
        selected_category =  models.category.objects.all()
        obj = products.objects.select_related('category').get(id = id)
        context = {
                    'items':obj,
                    'cat':selected_category,
                }
        if request.method == 'POST':
                name = request.POST['name']
                category = request.POST['category']
                selected_category =  models.category.objects.get(id = category)
                quantity = request.POST['quantity']
                price = request.POST['price']
                desc1 = request.POST['desc']
                img1 = request.FILES['img1'] if 'img1' in request.FILES else None
                img2 = request.FILES['img2'] if 'img2' in request.FILES else None
                img3 = request.FILES['img3'] if 'img3' in request.FILES else None
                img4 = request.FILES['img4'] if 'img4' in request.FILES else None
                if img1:
                      if  obj.img1:
                            os.remove(obj.img1.path)
                      obj.img1 = img1
                if img2:
                      if  obj.img2:
                            os.remove(obj.img2.path)
                      obj.img2 = img2
                if img3:
                      if  obj.img3:
                            os.remove(obj.img3.path)
                      obj.img3 = img3
                if img4:
                      if  obj.img4:
                            os.remove(obj.img4.path)
                      obj.img4 = img4
                obj.name = name
                obj.category = selected_category
                obj.quantity = quantity
                obj.price = price
                obj.description = desc1
                obj.save()
                messages.success(request, "product updated successfully")
                return redirect('adminproductmanage')
        return render(request,'edit_product.html',context)







# add product
def add_product(request):
    p = models.category.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        selected_category =  models.category.objects.get(id = category)
        quantity = request.POST['quantity']
        price = request.POST['price']
        desc1 = request.POST['description']
        img1 = request.FILES['img1'] if 'img1' in request.FILES else None
        img2 = request.FILES['img2'] if 'img2' in request.FILES else None
        img3 = request.FILES['img3'] if 'img3' in request.FILES else None
        img4 = request.FILES['img4'] if 'img4' in request.FILES else None
        obj = products(name = name,category = selected_category,quantity = quantity,price = price,description = desc1,img1 = img1,img2 = img2,img3 = img3,img4 = img4)
        obj.save()
        messages.success(request, "product added successfully")
        return redirect('adminproductmanage')
    return render(request,'add_product.html',{'cat' : p})





# delete product
def delete_product(request,id):
      products.objects.get(id = id).delete()
      messages.success(request, "product deleted successfully")
      return redirect('adminproductmanage')