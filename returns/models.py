from django.db import models
from products.models import Product
from staff.models import Staff
from branches.models import Branch


class ProductReturn(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    returned = models.DateTimeField(auto_now_add=True)
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)

    def __str__(self):

        return self.product.name
