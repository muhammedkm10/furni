from django.shortcuts import render,redirect,HttpResponse
from .models import category
from django.contrib import messages

# Create your views here.
# show category
def show_category(request):
    if 'email' not in request.session:
       if 'username' in request.session:
            items = category.objects.all()
            context = {
                'items' : items
            }
            return render(request,'category_manage.html',context)
       else:
           return redirect('adminlogin')
    else:
     return render(request, '404.html', status=404)






# add category
def add_category(request):
    if request.method == 'POST':
        name2 = request.POST['nameeee']
        description = request.POST['desc'] 
        o = category.objects.filter(name  = name2).exists()
        if not o:
            items = category(name = name2,description = description)
            items.save()
            messages.success(request, "category added successfully")
            return redirect('category')
        else:
            messages.error(request, "category is already in the table...")
            return redirect('category')

    



# edit category
def edit_category(request,id):
    if request.method == 'POST':
          name1 = request.POST['halo1']
          description = request.POST['desc']
          items = category(id = id,name = name1,description = description)
          items.save()
          messages.success(request, "category edited successfully")
          return redirect('category')
    return redirect('category_manage.html')




# search category
def search(request):
    if request.method == 'POST':
        query = request.POST['qry']
        obj = category.objects.filter(name__icontains=query)
        context = {
            'items':obj
        }
    return render(request,'category_manage.html',context)



# list category
def list_category(request,id):
    obj = category.objects.get(id = id)
    obj.is_listed = True
    obj.save()
    return redirect('category')


# un list category
def un_list_category(request,id):
    obj = category.objects.get(id = id)
    obj.is_listed = False
    obj.save()
    return redirect('category')

   
