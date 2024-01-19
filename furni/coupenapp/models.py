from django.db import models

# Create your models here.
class coupons(models.Model):
    cop_name = models.CharField(max_length=50)
    cop_price = models.BigIntegerField()
    code = models.CharField( max_length=50)
    from_date = models.DateField()
    to = models.DateField()
    is_listed = models.BooleanField(default = True)