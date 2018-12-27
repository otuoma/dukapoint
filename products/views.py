from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView, FormView, UpdateView, DeleteView, DetailView
from products.models import Product
from products.forms import CreateProductForm, UpdateProductForm
from django.contrib import messages


class ProductDetail(PermissionRequiredMixin, DetailView):
    permission_required = ['products.view_product']
    raise_exception = True
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        item = context['product']

        context['stock_vals'] = {
            'cost_value': item.buying_price * item.quantity,
            'retail_value': item.retail_price * item.quantity,
            'wholesale_value': item.wholesale_price * item.quantity,
        }

        return context


class DeleteProduct(PermissionRequiredMixin, DeleteView):
    permission_required = ['products.delete_product']
    raise_exception = True
    model = Product

    def get_success_url(self):

        messages.success(self.request, 'Success, product deleted.', extra_tags='alert alert-info')

        return reverse_lazy(viewname='products:home')


class UpdateProduct(PermissionRequiredMixin, UpdateView):
    permission_required = ['products.change_product']
    raise_exception = True
    form_class = UpdateProductForm
    template_name = 'products/edit_product.html'
    model = Product

    def get_success_url(self):

        messages.success(self.request, 'Success, product updated.', extra_tags='alert alert-success')

        return reverse_lazy(viewname='products:update-product', kwargs={'pk': self.kwargs['pk']})


class CreateProduct(PermissionRequiredMixin, FormView):
    permission_required = 'products.add_product'
    raise_exception = True
    template_name = 'products/create_product.html'
    form_class = CreateProductForm

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, 'Success, product created', extra_tags='alert alert-success')

            return redirect(to='products:create-product')
        else:
            products = Product.objects.all().order_by('-pk')[:20]

            p_list = []
            num = 0

            if products.count() > 0:

                for product in products:
                    num = num + 1

                    p_list.append({
                        'num': num,
                        'name': product.name,
                        'sku_code': product.sku_code,
                        'description': product.description,
                        'manufacturer': product.manufacturer,
                        'supplier': product.supplier,
                        'pk': product.pk,
                    })

            context = {
                'products': p_list,
                'form': form
            }

            messages.error(request, 'Failed, product not created', extra_tags='alert alert-danger')

            return render(request, self.template_name, context=context)

    def get(self, request, *args, **kwargs):

        products = Product.objects.all().order_by('-pk')[:20]

        p_list = []
        num = 0

        if products.count() > 0:

            for product in products:
                num = num + 1

                p_list.append({
                    'num': num,
                    'name': product.name,
                    'sku_code': product.sku_code,
                    'description': product.description,
                    'manufacturer': product.manufacturer,
                    'supplier': product.supplier,
                    'pk': product.pk,
                })

        context = {
            'products': p_list,
            'form': self.form_class
        }

        return render(request, self.template_name, context=context)


class Home(PermissionRequiredMixin, TemplateView):
    template_name = 'products/home.html'
    permission_required = ['products.add_product']
    raise_exception = True

    def get(self, request, *args, **kwargs):

        products = Product.objects.all().order_by('-pk')

        p_list = []
        num = 0

        if products.count() > 0:

            for product in products:

                num = num + 1

                p_list.append({
                    'num': num,
                    'name': product.name,
                    'sku_code': product.sku_code,
                    'quantity': product.quantity,
                    'manufacturer': product.manufacturer,
                    'supplier': product.supplier,
                    'created': product.created,
                    'pk': product.pk,
                })

        context = {
            'products': p_list
        }

        return render(request, self.template_name, context=context)

