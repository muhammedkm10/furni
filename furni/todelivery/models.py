from django.db import models
from logintohome.models import  CustomUser1
from product_manage.models import products

# Create your models here.

class address(models.Model):
    user_id = models.ForeignKey(CustomUser1,on_delete = models.CASCADE)
    first_name = models.CharField( max_length=200)
    last_name = models.CharField( max_length=200)
    country = models.CharField( max_length=200)
    state = models.CharField( max_length=200)
    address = models.TextField()
    pin = models.BigIntegerField()
    post = models.CharField( max_length=200)
    email = models.EmailField()
    phone = models.BigIntegerField()
    is_cancelled = models.BooleanField(default = False)


class order_details(models.Model):
    user_id = models.ForeignKey(CustomUser1, on_delete=models.CASCADE)
    pay_method = models.CharField(max_length = 50)
    order_date = models.DateField()
    addres = models.TextField()


class ordered_items(models.Model):
    order_id = models.ForeignKey(order_details,on_delete=models.CASCADE )
    product_name =  models.ForeignKey(products, on_delete=models.CASCADE)
    quantity =  models.IntegerField()
    status =  models.CharField(max_length = 50)
    total_amount =models.IntegerField()
    category  =  models.CharField(max_length = 50)
    user = models.IntegerField()
    add = models.ForeignKey(address, on_delete=models.CASCADE)
    expected = models.DateField(null = True )



    





    