from django.db import models
from logintohome.models import CustomUser1
from product_manage.models import products
from todelivery.models import order_details, ordered_items

# Create your models here.


class wallet(models.Model):
    user_id = models.ForeignKey(CustomUser1, on_delete=models.CASCADE)
    amount = models.BigIntegerField(default=0)


class product_review(models.Model):
    user_id = models.ForeignKey(CustomUser1, on_delete=models.CASCADE)
    pro_id = models.ForeignKey(products, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()


class return_requests(models.Model):
    user_id = models.ForeignKey(CustomUser1, on_delete=models.CASCADE)
    order_id = models.ForeignKey(order_details, on_delete=models.CASCADE)
    item_id = models.ForeignKey(ordered_items, on_delete=models.CASCADE)
    reason = models.TextField()
    return_date = models.DateField(null = True)
    pickup_date = models.DateField(null = True)

