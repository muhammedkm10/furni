from django.shortcuts import render,redirect
from django.contrib import messages
from .models import coupons

# coupen manage
def coupen_manage(request):
    if 'email' not in request.session:
       obj = coupons.objects.all()
       context = {
          'cop':obj,
       }
       return render(request,'coupen_manage.html',context)
    else:
       return render(request, '404.html', status=404)
    
# add coupon
def add_coupon(request):
   if request.method == 'POST':
      name = request.POST['name']
      price = request.POST['price']
      code = request.POST['code']
      fromdate = request.POST['from']
      todate = request.POST['to']
      coupons.objects.create(cop_name =name,cop_price = price,code = code,from_date = fromdate,to = todate)
      messages.success(request,'your coupen added successfully')
      return redirect('coupenmanage')
   
# edit coupon
def edit_coupon(request,id):
   if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        code = request.POST['code']
        fromdate = request.POST['from']
        todate = request.POST['to']
        obj  = coupons.objects.get(id = id)
        obj.cop_name = name
        obj.cop_price = price
        obj.code = code
        obj.from_date = fromdate
        obj.to = todate
        obj.save()
        messages.success(request,'your coupen edited successfully')
        return redirect('coupenmanage')



# delete coupon
def delete_coupon(request,id):
   if request.method == 'POST':
        coupons.objects.get(id = id).delete()
        messages.error(request,'coupon deleted succesfully')
        return redirect('coupenmanage')
        


# list coup[en]
def list_coupen(request,id):
    obj = coupons.objects.get(id = id)
    obj.is_listed = True
    obj.save()
    return redirect('coupenmanage')


# un list category
def un_list_coupen(request,id):
    obj = coupons.objects.get(id = id)
    obj.is_listed = False
    obj.save()
    return redirect('coupenmanage')