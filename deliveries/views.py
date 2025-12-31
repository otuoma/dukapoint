from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, FormView, TemplateView
from deliveries.models import Delivery, Stock
from deliveries.forms import SetSupplierForm, DeliveryForm, DeliveriesFiltersForm
from products.models import Product, BranchProduct
from suppliers.models import Supplier
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib import messages
from deliveries.utils import delivery_value


class ListDeliveryItems(PermissionRequiredMixin, ListView):
    permission_required = ["delivery.view_delivery"]
    raise_exception = True
    permission_denied_message = "You dont have permission to view deliveries"
    template_name = "deliveries/delivery_items.html"
    model = Stock
    context_object_name = "stock_list"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        stock_queryset = Stock.objects.filter(delivery_id=self.kwargs['delivery_id'])
        delivery = get_object_or_404(Delivery, pk=self.kwargs['delivery_id'])
        stock = list()
        num = 0

        for item in stock_queryset:

            total_cost = item.quantity * item.buying_price
            num += 1

            stock.append({
                "num": num,
                "product_id": item.product_id,
                "product_name": item.product.name,
                "buying_price": item.buying_price,
                "quantity": item.quantity,
                "total_cost": total_cost
            })

        context['stock_list'] = stock
        context['delivery'] = delivery

        return context


class PostStock(PermissionRequiredMixin, TemplateView):
    """Saves data to the database"""
    permission_required = ['delivery.add_delivery']
    raise_exception = True
    permission_denied_message = "You dont have permission to add delivery"

    def get(self, request, *args, **kwargs):

        try:
            products = request.session['products']
        except KeyError:

            messages.error(request, "No products have been added", extra_tags="alert alert-danger")

            return redirect(to="/deliveries/create-delivery-note/")

        supplier = get_object_or_404(Supplier, pk=request.session['supplier']['supplier_id'])
        del_val = delivery_value(products)

        delivery = Delivery(
            received_from_id=supplier.pk,
            processed_by_id=request.user.pk,
            branch_id=request.user.branch.pk,
            value=del_val,
            delivery_number=request.session['supplier']['delivery_number']
        )

        delivery.save()

        for item in products:

            product = get_object_or_404(Product, pk=item['product_id'])

            product.quantity = product.quantity + item['quantity']

            product.save()

            stock = Stock(
                product_id=product.pk,
                quantity=item['quantity'],
                buying_price=item['buying_price'],
                retail_price=item['retail_price'],
                wholesale_price=item['wholesale_price'],
                current_branch_id=request.user.branch.pk,
                home_branch_id=request.user.branch.pk,
                delivery_id=delivery.pk,
                staff_id=request.user.pk
            )

            stock.save()

            # Update branch_stock tbl

            branch_stock, created = BranchProduct.objects.get_or_create(
                product_id=product.pk,
                branch_id=request.user.branch.pk
            )

            branch_stock.quantity = branch_stock.quantity + item['quantity']

            branch_stock.save()

        messages.success(request, "Success, products stock has been updated.", extra_tags="alert alert-success")

        del request.session['products']
        del request.session['supplier']

        return redirect(to="/deliveries/")


class CreateDeliveryNote(PermissionRequiredMixin, FormView):
    permission_required = ['delivery.add_delivery']
    raise_exception = True
    permission_denied_message = "You dont have permission to add delivery"
    template_name = "deliveries/create_delivery_note.html"
    form_class = DeliveryForm

    def get(self, request, *args, **kwargs):

        context = super().get_context_data(**kwargs)

        if "supplier" not in request.session.keys():

            return redirect(to="/deliveries/set-supplier/")

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        form = DeliveryForm(data=request.POST)

        context = self.get_context_data(**kwargs)

        if "products" not in request.session.keys():

            messages.error(request, "Set the supplier to proceed", extra_tags="alert alert-danger")

            return redirect(to="/deliveries/set-supplier/")

        products_list = request.session['products']
        product_ids = [pk['product_id'] for pk in products_list]

        if form.is_valid():

            product = get_object_or_404(Product, pk=form.cleaned_data['product'])

            if len(products_list) == 0:  # add initial product

                num = len(products_list) + 1
                products_list.append({
                    "num": num,
                    "product_name": product.name,
                    "product_id": product.pk,
                    "quantity": form.cleaned_data['quantity'],
                    "buying_price": form.cleaned_data['buying_price'],
                    "retail_price": form.cleaned_data['retail_price'],
                    "wholesale_price": form.cleaned_data['wholesale_price'],
                    "total_cost": form.cleaned_data['buying_price'] * form.cleaned_data['quantity'],
                })
            else:  # products_list has items, loop through

                if product.pk not in product_ids:
                    num = len(products_list) + 1

                    products_list.append({
                        "num": num,
                        "product_name": product.name,
                        "product_id": product.pk,
                        "quantity": form.cleaned_data['quantity'],
                        "buying_price": form.cleaned_data['buying_price'],
                        "retail_price": form.cleaned_data['retail_price'],
                        "wholesale_price": form.cleaned_data['wholesale_price'],
                        "total_cost": form.cleaned_data['buying_price'] * form.cleaned_data['quantity'],
                    })
                else:

                    for item in products_list:

                        if item['product_id'] == product.pk:

                            item['quantity'] = form.cleaned_data['quantity']
                            item['buying_price'] = form.cleaned_data['buying_price']
                            item['retail_price'] = form.cleaned_data['retail_price']
                            item['wholesale_price'] = form.cleaned_data['wholesale_price']
                            item['total_cost'] = form.cleaned_data['buying_price'] * form.cleaned_data['quantity']

            request.session['products'] = products_list

            return redirect(to="/deliveries/create-delivery-note/")

        else:  # form is invalid

            request.session['products'] = products_list

        context['products_list'] = request.session['products']

        return render(request, self.template_name, context=context)


class SetSupplier(PermissionRequiredMixin, FormView):
    permission_required = ["delivery.add_delivery"]
    raise_exception = True
    permission_denied_message = "You dont have permission to add deliveries"
    template_name = "deliveries/set_supplier.html"
    form_class = SetSupplierForm

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():

            supplier = form.cleaned_data['supplier']

            request.session['supplier'] = {
                "supplier_id": supplier.pk,
                "supplier_name":supplier.name,
                "delivery_number": form.cleaned_data['delivery_number']
            }
            request.session['products'] = list()

        return redirect(to='/deliveries/create-delivery-note')


class SearchProduct(PermissionRequiredMixin, FormView):
    permission_required = ["deliveries.create_delivery"]
    raise_exception = True
    permission_denied_message = "You dont have permission to add deliveries"

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


class ClearDeliveryNote(PermissionRequiredMixin, TemplateView):
    permission_required = ['delivery.add_delivery']
    raise_exception = True
    permission_denied_message = "You dont have permission to add deliveries"

    def get(self, request, *args, **kwargs):

        if 'products' in request.session.keys():

            del request.session['products']
        else:
            pass

        return redirect(to='/deliveries/create-delivery-note/')


class Home(PermissionRequiredMixin, FormView):
    """Displays deliveries and filters deliveries based on submitted form"""

    permission_required = ['delivery.view_delivery']
    raise_exception = True
    permission_denied_message = "You dont have permission to view deliveries"
    form_class = DeliveriesFiltersForm

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)

        context['delivery_list'] = Delivery.objects.all().order_by("-date")[:500]

        return render(request, "deliveries/home.html", context)

    def post(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)

        form = self.form_class(data=request.POST)

        if form.is_valid():

            queryset = Delivery.objects.filter(
                date__gte=form.cleaned_data['date_from'],
                date__lte=form.cleaned_data['date_to'],
                branch=form.cleaned_data['branch']
            )

            context['delivery_list'] = queryset

        return render(request, "deliveries/home.html", context)

