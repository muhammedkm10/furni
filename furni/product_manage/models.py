from django.db import models
from category_management.models import category


# Create your models here.

class products(models.Model):

    name = models.CharField(max_length=200)
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField()
    img1 =  models.ImageField(upload_to='images/')
    img2 =  models.ImageField(upload_to='images/')
    img3 =  models.ImageField(upload_to='images/')
    img4 =  models.ImageField(upload_to='images/')
    is_listed = models.BooleanField(default = True)
    original_price = models.IntegerField(null = True)



    def __str__(self):
        return self.name
class variant(models.Model):
    product_id = models.ForeignKey(products,on_delete = models.CASCADE)
    size = models.CharField(max_length=4)
    quantity = models.IntegerField()