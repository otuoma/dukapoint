from django.db import models
from suppliers.models import Supplier
from branches.models import Branch
# from deliveries.models import Delivery
from staff.models import Staff


class Product(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    manufacturer = models.CharField(max_length=150, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    sku_code = models.CharField(max_length=25, unique=True)
    product_image = models.ImageField(upload_to='product_images', blank=True)
    quantity = models.IntegerField(default=0, help_text="Quantity in stock")

    buying_price = models.FloatField(default=0.0)
    retail_price = models.FloatField(default=0.0)
    wholesale_price = models.FloatField(default=0.0)

    def __str__(self):

        return self.name


class BranchProduct(models.Model):
    """Purposely for keeping track of product quantity at a branch"""

    product = models.ForeignKey(Product, on_delete=models.PROTECT, unique=False,)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, unique=False)
    quantity = models.IntegerField(default=0.0)

    def __str__(self):

        return self.product.name


class Transfer(models.Model):
    """A container for products being transfered"""
    transfer_from = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='transfer_from')
    transfer_to = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='transfer_to')
    transfer_date = models.DateTimeField(auto_now_add=True)
    date_received = models.DateTimeField(blank=True, null=True)
    received = models.BooleanField(default=False)
    value = models.FloatField(default=0.0)
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):

        return str(self.transfer_date)

    def get_products(self):

        """return queryset of products belonging to this transfer"""

        return TransferProduct.objects.filter(transfer=self.pk)

    class Meta:
        permissions = [('receive_transfer', 'Can receive transfer')]


class TransferProduct(models.Model):
    """The individual product instance being transfered"""
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    transfer = models.ForeignKey(Transfer, on_delete=models.PROTECT)
    unit_cost = models.FloatField(default=0.0)

    def __str__(self):

        return self.product.name

