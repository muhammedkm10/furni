from django.db import models
from product_manage.models import products
from category_management.models import category

# Create your models here.

class  product_offer(models.Model):
    pro_id = models.ForeignKey(products,on_delete = models.CASCADE)
    percentage = models.IntegerField()
    is_listed = models.BooleanField(default = True)





class  category_offer(models.Model):
    cat_id = models.ForeignKey(category,on_delete = models.CASCADE)
    percentage = models.IntegerField()
    is_listed = models.BooleanField(default = True)
