from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from datetime import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView, FormView, UpdateView, DeleteView, DetailView, ListView
from products.models import Product, Transfer, TransferProduct, BranchProduct
from deliveries.models import Stock, Delivery
from suppliers.models import Supplier
from products.forms import CreateProductForm, UpdateProductForm, TransferFiltersForm, ProductTransferForm, SetTransferToForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


class ReceiveTransfer(PermissionRequiredMixin, TemplateView):
    permission_required = ['transfer.receive_transfer']
    raise_exception = True
    permission_denied_message = "You dont have permission to receive transfer"
    template_name = 'products/receive_transfer.html'

    def get(self, request, *args, **kwargs):

        context = dict()

        transfer = get_object_or_404(Transfer, pk=self.kwargs['transfer_id'])
        transfer_products = TransferProduct.objects.filter(transfer_id=self.kwargs['transfer_id'])

        context['transfer_products'] = transfer_products
        context['transfer'] = transfer

        if request.GET.get("type") == "as_is":

            if transfer.received:  # Prevent repeat if page is reloaded
                return redirect(to=f"/products/receive_transfer/{transfer.pk}/")

            # Add entry in deliveries
            received_from = get_object_or_404(Supplier, name=transfer.transfer_from.name)
            delivery = Delivery(
                received_from_id=received_from.pk,
                value=transfer.value,
                processed_by_id=request.user.pk,
                delivery_number="TRANSFER",
                is_transfer=True,
                branch_id=request.user.branch_id
            )
            delivery.save()

            for product in transfer_products:

                branch_product, created = BranchProduct.objects.get_or_create(
                    product_id=product.pk,
                    branch_id=transfer.transfer_to.pk
                )

                branch_product.quantity = branch_product.quantity + product.quantity

                branch_product.save()

                # create stock instance
                product_details = get_object_or_404(Stock, product_id=product.product_id, current_branch_id=transfer.transfer_from_id)
                stock = Stock(
                    quantity=product.quantity,
                    buying_price=product_details.buying_price,
                    retail_price=product_details.retail_price,
                    wholesale_price=product_details.wholesale_price,
                    current_branch_id=request.user.branch_id,
                    delivery_id=delivery.pk,
                    home_branch_id=request.user.branch_id,
                    product_id=product.product_id,
                    staff_id=request.user.pk
                )
                stock.save()

            transfer.received = True
            transfer.date_received = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transfer.save()

            messages.success(request, "Success, items have been received", extra_tags="alert alert-success")

        return render(request, self.template_name, context=context)


class ViewTransferProducts(PermissionRequiredMixin, TemplateView):
    permission_required = ['transfer.view_transfer']
    permission_denied_message = "You dont have permission to view transfers"
    raise_exception = True
    template_name = "products/view_transfer_items.html"
    context_object_name = "transfer_products"

    def get(self, request, *args, **kwargs):

        context = dict()

        transfer = get_object_or_404(Transfer, pk=self.kwargs['transfer_id'])

        context['transfer'] = transfer

        context['transfer_products'] = transfer.get_products()

        return render(request, self.template_name, context=context)


class ProcessTransfer(PermissionRequiredMixin, FormView):
    permission_required = ['transfer.add_transfer']
    permission_denied_message = "You dont have permission to add transfers"
    raise_exception = True
    template_name = 'products/transfer_products.html'
    form_class = ProductTransferForm

    def get(self, request, *args, **kwargs):

        if "products" not in request.session.keys():
            return redirect(to='/products/view-transfers/')

        list_products = request.session['products']

        transfer = Transfer(
            transfer_from_id=request.user.branch_id,
            transfer_to_id=request.session['transfer_to_id'],
            staff_id=request.user.pk,
        )

        transfer.save()

        value = 0.0

        for product in list_products:

            item = Stock.objects.filter(
                product_id=product['product_id'],
                home_branch_id=request.user.branch_id
            ).last()

            # Update Product model
            product_instance = get_object_or_404(Product, pk=product['product_id'])
            product_instance.quantity -= product['quantity']
            product_instance.save()

            # Update transfer_product tbl
            transfer_product = TransferProduct(
                transfer_id=transfer.pk,
                product_id=product['product_id'],
                unit_cost=item.buying_price,
                quantity=product['quantity']
            )

            transfer_product.save()
            value += product['quantity'] * item.buying_price

            # Update branch_stock tbl
            branch_stock = BranchProduct.objects.get(
                branch_id=request.user.branch_id,
                product_id=product['product_id']
            )

            branch_stock.quantity -= product['quantity']
            branch_stock.save()

        transfer.value = value
        transfer.save()

        del request.session['products']
        del request.session['transfer_to_id']

        return redirect(to='/products/view-transfers/')


class ViewTransfers(PermissionRequiredMixin, ListView):
    permission_required = ['transfer.view_transfer']
    permission_denied_message = "You dont have permission to view transfers"
    raise_exception = True
    template_name = 'products/view_transfers.html'
    form_class = TransferFiltersForm
    context_object_name = "transfers_list"

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)

        context['form'] = self.form_class

        return context

    def get_queryset(self):

        q = Transfer.objects.all()
        # q = Transfer.objects.filter(transfer_from_id=self.request.user.branch_id)

        return q


class AddProduct(PermissionRequiredMixin, FormView):
    """Add product item to session cart"""
    permission_required = ['transfer.add_transfer']
    permission_denied_message = "You dont have permission to add transfers"
    raise_exception = True
    template_name = 'products/transfer_products.html'
    form_class = ProductTransferForm

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():

            product = get_object_or_404(Product, pk=form.cleaned_data['product'])

            try:
                stock = Stock.objects.filter(
                    product_id=product.pk,
                    home_branch_id=request.user.branch_id,
                    current_branch_id=request.user.branch_id
                ).latest('posted')

            except ObjectDoesNotExist:

                messages.error(request, "Out of stock, no purchases on record", extra_tags="alert alert-danger")

                return redirect(to='/products/transfer-products/')

            if stock.quantity < form.cleaned_data['quantity']:

                messages.error(
                    request,
                    f"Out of range, only {stock.quantity} available.",
                    extra_tags="alert alert-danger"
                )

                return redirect(to='/products/transfer-products/')

            new_product = {
                'product_name': product.name,
                'product_id': product.pk,
                'unit_cost': stock.buying_price,
                'quantity': form.cleaned_data['quantity'],
                'total': form.cleaned_data['quantity'] * stock.buying_price,
            }

            if "products" not in request.session:  # first product

                request.session['products'] = list()

                request.session['products'].append(new_product)

                request.session['products_total'] = new_product['total']

            else:

                cart_products = request.session['products']
                product_ids = [pk['product_id'] for pk in cart_products]

                if new_product['product_id'] not in product_ids:

                    cart_products.append(new_product)

                else:

                    for item in cart_products:

                        if item['product_id'] == new_product['product_id']:

                            item['quantity'] = item['quantity'] + new_product['quantity']
                            item['total'] = item['quantity'] * item['unit_cost']

                        else:
                            pass

                request.session['products'] = cart_products
                request.session['products_total'] = sum([item['total'] for item in cart_products])

        return redirect(to='/products/transfer-products/')


class TransferProducts(PermissionRequiredMixin, FormView):

    """Only displays the template ie form and list"""

    permission_required = ['transfer.add_transfer']
    raise_exception = True
    permission_denied_message = "You dont have permission to add transfers"
    template_name = 'products/transfer_products.html'
    form_class = ProductTransferForm

    def get(self, request, *args, **kwargs):

        if "transfer_to_id" not in self.request.session.keys():

            return redirect(to="/products/set-transfer-to/")
        else:

            return render(request, self.template_name, context=self.get_context_data())


class ProductDetail(PermissionRequiredMixin, DetailView):
    permission_required = ['products.view_product']
    permission_denied_message = "You dont have permission to view products"
    raise_exception = True
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        product = context['product']

        branch_stock, created = BranchProduct.objects.get_or_create(
            branch_id=self.request.user.branch_id,
            product_id=product.pk
        )

        try:
            stock = Stock.objects.filter(
                product_id=product.pk,
                home_branch_id=self.request.user.branch_id,
                current_branch_id=self.request.user.branch_id
            ).latest('posted')

            buying_price = stock.buying_price
            retail_price = stock.retail_price
            wholesale_price = stock.wholesale_price
            supplier = stock.delivery.received_from.name

        except ObjectDoesNotExist:

            buying_price = 0.0
            retail_price = 0.0
            wholesale_price = 0.0
            supplier = product.supplier.name

        context['stock_vals'] = {
            'cost_value': buying_price * branch_stock.quantity,
            'retail_value': retail_price * branch_stock.quantity,
            'retail_price': retail_price,
            'wholesale_price': wholesale_price,
            'wholesale_value': wholesale_price * product.quantity,
            'quantity': branch_stock.quantity,
            'buying_price': buying_price,
            'supplier': supplier,
        }

        return context


class DeleteProduct(PermissionRequiredMixin, DeleteView):
    permission_required = ['products.delete_product']
    permission_denied_message = "You dont have permission to delete product"
    raise_exception = True
    model = Product

    def get_success_url(self):

        messages.success(self.request, 'Success, product deleted.', extra_tags='alert alert-info')

        return reverse_lazy(viewname='products:home')


class UpdateProduct(PermissionRequiredMixin, UpdateView):
    permission_required = ['products.change_product']
    permission_denied_message = "You dont have permission to change product"
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
    permission_denied_message = "You dont have permission to add products"
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
    permission_denied_message = "You dont have permission to view products"
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


class DeleterCartProduct(PermissionRequiredMixin, TemplateView):
    permission_required = ["transfer.add_transfer"]
    permission_denied_message = "You dont have permission to add transfers"
    raise_exception = True

    def get(self, request, *args, **kwargs):

        if not self.kwargs['product_id']:

            return redirect(to='/products/transfer-products/')

        if 'products' in request.session.keys():

            if self.kwargs['product_id'] in [p['product_id'] for p in request.session['products']]:

                cart_products = request.session['products']

                for product in cart_products:

                    if product['product_id'] == self.kwargs['product_id']:

                        cart_products.remove(product)

                        request.session['products'] = cart_products
                        request.session['products_total'] = sum([item['total'] for item in cart_products])

                        messages.success(request, 'Success, product has been removed', extra_tags='alert alert-info')

            else:

                messages.error(request, 'Product not in list', extra_tags='alert alert-danger')
        else:
            messages.info(request, 'Alert!, list is empty', extra_tags='alert alert-info')

        return redirect(to='/products/transfer-products/')


class ClearList(PermissionRequiredMixin, TemplateView):
    permission_required = ["transfer.add_transfer"]
    permission_denied_message = "You dont have permission to add transfers"
    raise_exception = True

    def get(self, request, *args, **kwargs):

        if 'products' in request.session.keys():

            del request.session['products']
        else:
            pass

        return redirect(to='/products/transfer-products/')


class SetTransferTo(PermissionRequiredMixin, FormView):
    permission_required = ["transfer.add_transfer"]
    permission_denied_message = "You dont have permission to add transfers"
    raise_exception = True
    template_name = 'products/set_transfer_to.html'
    form_class = SetTransferToForm

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():

            if form.cleaned_data['transfer_to'].pk == request.user.branch_id:

                messages.error(request, "Can not transfer to same branch", extra_tags="alert alert-danger")

                return redirect(to="/products/set-transfer-to/")

            request.session['transfer_to'] = form.cleaned_data['transfer_to'].name
            request.session['transfer_to_id'] = form.cleaned_data['transfer_to'].pk

            return redirect(to="/products/add-product/")
        else:

            return render(request, self.template_name, self.get_context_data())
