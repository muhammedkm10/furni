from django.db import models
from logintohome.models import CustomUser1
from product_manage.models import products

# Create your models here.
class cart(models.Model):
    user_id = models.ForeignKey(CustomUser1, on_delete = models.CASCADE)
    product_id = models.ForeignKey(products,on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    total = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.product_id.name} - {self.quantity}'
    
    def subtotal(self):
        return self.product_id.price*self.quantity
    

    