from django.db import models
from category_management.models import category


# Create your models here.


class products(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField()
    img1 = models.ImageField(upload_to="images/")
    img2 = models.ImageField(upload_to="images/")
    img3 = models.ImageField(upload_to="images/")
    img4 = models.ImageField(upload_to="images/")
    is_listed = models.BooleanField(default=True)
    original_price = models.IntegerField(null=True)

    def calculate_discounted_price(self):
        cat_offer = self.category.category_offer_set.first()
        pro_offer = self.product_offer_set.first()

        if pro_offer and cat_offer:
            if pro_offer.is_listed == True and cat_offer.is_listed == True:
                a = self.price - (pro_offer.percentage / 100) * self.price
                b = self.price - (cat_offer.percentage / 100) * self.price
                c = int(min(a, b))
                return c
            elif pro_offer.is_listed == True and cat_offer.is_listed == False:
                a = self.price - (pro_offer.percentage / 100) * self.price
                return int(a)
            elif pro_offer.is_listed == False and cat_offer.is_listed == True:
                a = self.price - (cat_offer.percentage / 100) * self.price
                return int(a)
            else:
                return self.price
        elif pro_offer:
            if pro_offer.is_listed:
                p = self.price - (pro_offer.percentage / 100) * self.price
                return int(p)
            else:
                return self.price
        elif cat_offer:
            if cat_offer.is_listed == True:
                return int(self.price - (cat_offer.percentage / 100) * self.price)
            else:
                return self.price
        else:
            return self.price

    def __str__(self):
        return self.name


class variant(models.Model):
    product_id = models.ForeignKey(products, on_delete=models.CASCADE)
    size = models.CharField(max_length=4)
    quantity = models.IntegerField()
