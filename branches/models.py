from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=150)
    branch_code = models.CharField(max_length=25, unique=True)
    location = models.CharField(max_length=150)
    phone_contact = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.name

