from django.db import models
from suppliers.models import Supplier
from branches.models import Branch
from staff.models import Staff


class Product(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    manufacturer = models.CharField(max_length=150, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    sku_code = models.CharField(max_length=25, unique=True)
    product_image = models.ImageField(upload_to='product_images', blank=True)
    quantity = models.IntegerField(default=0, help_text="Quantity in stock")

    buying_price = models.FloatField(default=1.0)
    retail_price = models.FloatField(default=0.0)
    wholesale_price = models.FloatField(default=0.0)

    def __str__(self):

        return self.name

