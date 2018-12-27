from django.db import models
from products.models import Product
from customers.models import Customer
from staff.models import Staff
from branches.models import Branch


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    datetime = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.PROTECT)
    unit_price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=1)
    total = models.FloatField(default=0.0)
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, null=True)

    def __str__(self):

        return self.product.name


