from django.shortcuts import render
from returns.models import ProductReturn
from django.views.generic import ListView, FormView
from django.views.generic.edit import CreateView
from returns.forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin
from products.models import Product
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


class ViewReturns(ListView):
    template_name = "returns/home.html"
    model = ProductReturn
    context_object_name = "products"


class AddReturn(PermissionRequiredMixin, FormView):
    permission_required = ["returns.add_productreturn"]
    raise_exception = True
    permission_denied_message = "You dont have permission to add returns"

    model = ProductReturn
    context_object_name = "product"
    form_class = AddReturnForm
    template_name = "returns/add_return.html"


class SearchProduct(PermissionRequiredMixin, FormView):
    """Return json data only"""
    permission_required = ["returns.add_productreturn"]
    raise_exception = True
    permission_denied_message = "You dont have permission to add returns"

    def get(self, request, *args, **kwargs):

        try:

            products = Product.objects.filter(name__contains=request.GET.get('product'))

            product_list = []

            for item in products:

                product_list.append({"product_name": item.name, "product_id": item.pk, "description": item.description})

            response = json.dumps(product_list)

        except ObjectDoesNotExist as exp:

            err_str = str(exp) + str(" or not active")

            response = json.dumps({'err': err_str})

        return HttpResponse(response, content_type="text/json")

