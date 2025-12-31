from django.db import models
from staff.models import Staff
from branches.models import Branch
from suppliers.models import Supplier
from products.models import Product


class Delivery(models.Model):

    date = models.DateTimeField(auto_now_add=True, unique=True)
    received_from = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    processed_by = models.ForeignKey(Staff, on_delete=models.PROTECT)
    value = models.FloatField(default=0.0)
    delivery_number = models.CharField(blank=True, null=True, max_length=50)
    is_transfer = models.BooleanField(default=False)

    def __str__(self):

        return self.received_from.name

    class Meta:
        ordering = ["-date",]


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    posted = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0, help_text='Quantity received')
    buying_price = models.FloatField(default=1.0)
    retail_price = models.FloatField(default=0.0)
    wholesale_price = models.FloatField(default=0.0)
    current_branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    home_branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='home_location', blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, default=1)
    delivery = models.ForeignKey(Delivery, on_delete=models.PROTECT)

    def __str__(self):

        return self.product.name
