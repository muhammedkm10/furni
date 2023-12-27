from django.shortcuts import render,redirect
from logintohome.models import CustomUser1
from todelivery.models import address
from django.contrib import messages
# Create your views here.



# showing the details of user profile addresses user added and the other details
def show_user_profile(request):
    if 'email' in request.session:
     email1 = request.session['email']
     obj = CustomUser1.objects.get(email = email1)
     user = obj.id
     addr = address.objects.filter(user_id = user)

     context={
           'obj':obj,
           'addr':addr
     }
     return render(request,'user_profile.html',context)
    return render(request, '404.html', status=404)



# removing the addresses user added
def remove_address(request,id):
   address.objects.get(id = id).delete()
   return redirect('userprofile')
   

# adding new address
def add_address_in_user(request):
     if request.method == "POST":
           email1  =  request.session['email']
           obj = CustomUser1.objects.get(email = email1)
           fname = request.POST['fname']
           lname = request.POST['lname']
           addv = request.POST['address']
           state = request.POST['state']
           country = request.POST['country']
           post = request.POST['post']
           pin = request.POST['pin']
           email = request.POST['email']
           phone = request.POST['phone']
           addobj = address(user_id = obj,first_name = fname,last_name=lname,address=addv,state=state,country=country,post=post,pin=pin,email=email,phone=phone)
           addobj.save()
           messages.success(request,"address added successfully")
           return redirect('userprofile')
     return render(request,'add_address_in_user.html')
   

# edit address

def edit_address(request,id):
    obj = address.objects.get(id = id)
    context = {
            'obj':obj,
        }
    if request.method == 'POST':
           
           fname = request.POST['fname']
           lname = request.POST['lname']
           addv = request.POST['address']
           state = request.POST['state']
           country = request.POST['country']
           post = request.POST['post']
           pin = request.POST['pin']
           email = request.POST['email']
           phone = request.POST['phone']
           obj.first_name  = fname
           obj.last_name  = lname
           obj.address  = addv
           obj.state  = state
           obj.country  = country
           obj.pin  = pin
           obj.post  = post
           obj.email  = email
           obj.phone  = phone
           obj.save()
           messages.success(request,"address edited successfully")
           return redirect('userprofile')
    return render(request,'edit_address.html',context)




# edit profile
def edit_profile(request): 
    email1 = request.session['email']
    obj = CustomUser1.objects.get(email = email1)
    context = {
        'user':obj,
    }
    return render(request,'edit_userprofile.html')