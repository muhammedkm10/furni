from django.db import models
from logintohome.models import CustomUser1

# Create your models here.


class wallet(models.Model):
    user_id = models.ForeignKey(CustomUser1, on_delete=models.CASCADE)
    amount = models.BigIntegerField(default = 0)
