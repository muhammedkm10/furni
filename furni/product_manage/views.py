from django.shortcuts import render,redirect
from . models import products
from category_management import models
from django.contrib import messages
import os
from django.core.files.base import ContentFile
import base64
import re

# Create your views here.
def product_manage(request):
    if 'email' not in request.session:
      if 'username' in request.session:
            obj = products.objects.select_related('category').all().order_by('-id')
            context = {
                  'items':obj
            }
            return render(request,'product.html',context)
      else:
           return redirect('adminlogin')
    else: 
         return render(request, '404.html', status=404)
    


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
                ogprice = request.POST['ogprice']
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
                if int(quantity) > 0 and int(price) > 0 and int(ogprice):
                  obj.quantity = quantity
                  obj.price = price
                  obj.original_price = ogprice
                  obj.description = desc1
                  obj.save()
                  messages.success(request, "product updated successfully")
                  return redirect('adminproductmanage')
                else:
                     messages.success(request, "please enter a valid input for quantity or price please check it....")
                     return redirect('editproduct',obj.id)
                     
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
        ogprice = request.POST['ogprice']
        desc1 = request.POST['description']
        if 'croppedImageData' in request.POST:
            img1 = request.POST['croppedImageData']

            # Convert base64 data to file and save
            if img1:
                format, imgstr = img1.split(';base64,')
                ext = re.search(r'/(.*?)$', format).group(1)

                # Convert base64 string to a Django ContentFile
                decoded_file = base64.b64decode(imgstr)
                img_file = ContentFile(decoded_file, name=f'cropped_image.{ext}')

                # Save the image file to the desired model field (adjust this as per your model)
            #     obj.img1.save(f'cropped_image.{ext}', img_file, save=True)



        img2 = request.FILES['img2'] if 'img2' in request.FILES else None
        img3 = request.FILES['img3'] if 'img3' in request.FILES else None
        img4 = request.FILES['img4'] if 'img4' in request.FILES else None
        if int(quantity) > 0 and int(price) > 0 and int(ogprice) > 0: 
            if not products.objects.filter(name = name).exists():
                  obj = products(name = name,category = selected_category,quantity = quantity,price = price,description = desc1,img1 = img_file,img2 = img2,img3 = img3,img4 = img4,original_price = ogprice)
                  obj.save()
                  messages.success(request, "product added successfully")
                  return redirect('adminproductmanage')
            else:
               messages.error(request, "product already exists")
               return redirect('addproduct')  
        else:
             messages.error(request, "please enter a valid input for quantity or price please check it....")
             return redirect('addproduct')
    return render(request,'add_product.html',{'cat' : p})





# delete product
def delete_product(request,id):
      products.objects.get(id = id).delete()
      messages.success(request, "product deleted successfully")
      return redirect('adminproductmanage')


# search for product
def search_product(request):
      if request.method  == 'POST':
        query = request.POST['query']
        obj = products.objects.filter(name__icontains = query)
        context = {
              'items':obj
        }
        return render(request,'product.html',context)
      


# list product
def list_product(request,id):
      obj = products.objects.get(id = id)
      obj.is_listed = True
      obj.save()
      return redirect('adminproductmanage')


# unlist list product
def un_list_product(request,id):
      obj = products.objects.get(id = id)
      obj.is_listed = False
      obj.save()
      return redirect('adminproductmanage')

      



