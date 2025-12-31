from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500, blank=True)
    primary_phone = models.CharField(max_length=15, blank=True)
    secondary_phone = models.CharField(max_length=15, blank=True)
    national_id = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    additional_email = models.EmailField(max_length=50, blank=True)
    address = models.TextField(max_length=50, blank=True)
    additional_address = models.TextField(max_length=50, blank=True)
    date_created = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return self.name

