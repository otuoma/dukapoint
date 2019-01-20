from django.views.generic import TemplateView, FormView, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
import json
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from products.models import Product, BranchProduct
from sales.forms import AddToCartForm, SaleForm, SalesFiltersForm
from django.shortcuts import redirect, render
from django.contrib import messages
from sales.models import Sale
from django.db.models import Sum


class ReportsHome(PermissionRequiredMixin, FormView):
    permission_required = ["sales.view_sales"]
    raise_exception = True
    template_name = 'sales/reports_home.html'
    form_class = SalesFiltersForm

    def post(self, request, *args, **kwargs):

        context = super().get_context_data(**kwargs)

        form = self.form_class(data=request.POST)

        if form.is_valid():

            context['sale_list'] = Sale.objects.filter(
                datetime__gte=str(form.cleaned_data['date_from']) + " 00:00:00",
                datetime__lte=str(form.cleaned_data['date_to']) + " 23:59:59",
                branch_id=form.cleaned_data['branch']
            )

            context['sum'] = context['sale_list'].aggregate(Sum('total'))

        return render(request, self.template_name, context=context)

    def get(self, request, *args, **kwargs):

        context = super().get_context_data(**kwargs)

        if request.GET.get("date_from"):

            context['sale_list'] = Sale.objects.filter(
                datetime__gte=request.GET.get("date_from"),
                datetime__lte=request.GET.get("date_to"),
                branch_id=request.GET.get("branch")
            )
        else:
            context['sale_list'] = Sale.objects.all()

        context['sum'] = context['sale_list'].aggregate(Sum('total'))

        return render(request, self.template_name, context=context)


class CheckOut(PermissionRequiredMixin, FormView):
    permission_required = ["sales.add_sale"]
    raise_exception = True
    form_class = SaleForm
    template_name = 'sales/check_out.html'

    def post(self, request, *args, **kwargs):

        for product in request.session['cart_products']:

            product_obj = Product.objects.get(pk=product['product_id'])

            sale = Sale(
                product_id=product['product_id'],
                quantity=product['quantity'],
                unit_price=product['unit_price'],
                total=product['unit_price']*product['quantity'],
                staff_id=self.request.user.pk,
                branch_id=self.request.user.branch.pk,
            )

            sale.save()

            # Update product_stock
            product_obj.quantity = product_obj.quantity - product['quantity']
            product_obj.save()

            # Update branch_stock tbl

            branch_stock, created = BranchProduct.objects.get_or_create(
                product_id=product_obj.pk,
                branch_id=request.user.branch.pk
            )

            branch_stock.quantity = branch_stock.quantity - product['quantity']

            branch_stock.save()

        del request.session['cart_products']
        messages.success(request, 'Sale completed successfully', extra_tags='alert alert-success')

        return redirect(to='/sales/')

    def get(self, request, *args, **kwargs):

        if 'cart_products' in request.session.keys():
            data = request.session['cart_products']
        else:
            data = None

        return render(request, self.template_name, {'cart_products': data})


class DeleterCartProduct(PermissionRequiredMixin, TemplateView):
    permission_required = ["products.view_products"]
    raise_exception = True

    def get(self, request, *args, **kwargs):

        if 'cart_products' in request.session.keys():

            if self.kwargs['product_id'] in [p['product_id'] for p in request.session['cart_products']]:

                cart_products = request.session['cart_products']

                for product in cart_products:

                    if product['product_id'] == self.kwargs['product_id']:

                        cart_products.remove(product)

                        request.session['cart_products'] = cart_products

                        messages.success(request, 'Success, product has been removed', extra_tags='alert alert-info')

            else:

                messages.error(request, 'Product not in cart', extra_tags='alert alert-danger')
        else:
            messages.info(request, 'Alert!, shopping cart is empty', extra_tags='alert alert-info')

        return redirect(to='/sales/')


class AddToCart(PermissionRequiredMixin, FormView):
    permission_required = ["products.view_products"]
    raise_exception = True
    form_class = AddToCartForm

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():

            product_name = form.cleaned_data['product_name']
            quantity = form.cleaned_data['quantity']
            unit_price = form.cleaned_data['unit_price']
            product_id = form.cleaned_data['product_id']

            new_product = {
                'product_name': product_name,
                'product_id': product_id,
                'unit_price': unit_price,
                'total': quantity * unit_price,
                'quantity': quantity,
            }

            if 'cart_products' not in request.session.keys():  # add first product to cart_products list

                cart_products = list()

                cart_products.append(new_product)

                request.session['cart_products'] = cart_products

            else:

                cart_products = request.session['cart_products']
                product_ids = [pk['product_id'] for pk in cart_products]

                if new_product['product_id'] not in product_ids:

                    cart_products.append(new_product)
                else:

                    for product in cart_products:

                        quantity = product['quantity'] + new_product['quantity']
                        total = quantity * new_product['unit_price']

                        if product['product_id'] == new_product['product_id']:
                            product['quantity'] = quantity
                            product['unit_price'] = new_product['unit_price']
                            product['total'] = total

                request.session['cart_products'] = cart_products

        else:
            cart_products = {"error": form.errors}

        return HttpResponse(
            json.dumps(cart_products),
            content_type="text/json"
        )


class Home(PermissionRequiredMixin, TemplateView):

    template_name = 'sales/pos.html'
    permission_denied_message = "You dont have permission to access page"

    def has_permission(self):

        if self.request.user.is_staff or self.request.user.is_superuser:

            return True
        else:
            return False

    def get(self, request, *args, **kwargs):

        if 'cart_products' in request.session.keys():
            data = request.session['cart_products']
        else:
            data = None

        return render(request, self.template_name, {'cart_products': data})


class ClearCart(TemplateView):

    def get(self, request, *args, **kwargs):

        if 'cart_products' in request.session.keys():

            del request.session['cart_products']
        else:
            pass

        return redirect(to='/sales/')


class SearchProducts(PermissionRequiredMixin, FormView):
    permission_required = ["products.view_products"]
    raise_exception = True

    def get(self, request, *args, **kwargs):

        try:

            products = Product.objects.filter(name__contains=request.GET.get('product'))

            product_list = []

            for item in products:
                product_list.append({
                    'name': item.name,
                    'id': item.pk,
                    'quantity': item.quantity,
                    'retail_price': item.retail_price,
                    'wholesale_price': item.wholesale_price,
                    'buying_price': item.buying_price,
                })

            response = json.dumps(product_list)

        except ObjectDoesNotExist as exp:

            err_str = str(exp) + str(" or not active")

            response = json.dumps({'err': err_str})

        return HttpResponse(response, content_type="text/json")