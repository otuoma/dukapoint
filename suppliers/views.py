from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from suppliers.models import Supplier
from suppliers.forms import CreateSupplierForm, UpdateSupplierForm
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin


class DeleteSupplier(PermissionRequiredMixin, DeleteView):
    model = Supplier
    permission_required = ['suppliers.delete_supplier']
    permission_denied_message = "You dont have permission to delete supplier"
    raise_exception = True
    success_url = reverse_lazy('suppliers:home')

    def get_success_url(self):

        messages.success(self.request, "Success, supplier deleted", extra_tags="alert alert-info")

        return self.success_url


class UpdateSupplier(PermissionRequiredMixin, UpdateView):
    template_name = 'suppliers/edit_supplier.html'
    raise_exception = True
    permission_required = ['suppliers.change_supplier']
    permission_denied_message = "You dont have permission to change supplier"
    form_class = UpdateSupplierForm

    def get(self, request, *args, **kwargs):

        supplier = get_object_or_404(Supplier, pk=self.kwargs['pk'])

        context = {
            'form': self.form_class(instance=supplier),
            'supplier': supplier
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        supplier = get_object_or_404(Supplier, pk=self.kwargs['pk'])

        form = self.form_class(instance=supplier, data=request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, 'Supplier updated', extra_tags='alert alert-success')

            return redirect(to='suppliers:update-supplier', pk=supplier.pk)
        else:

            context = {
                'form': form,
                'supplier': supplier
            }

            messages.error(request, 'Errors occurred', extra_tags='alert alert-danger')

            return render(request, self.template_name, context=context)


class CreateSupplier(PermissionRequiredMixin, CreateView):
    model = Supplier
    template_name = 'suppliers/create_supplier.html'
    raise_exception = True
    permission_required = ['suppliers.add_supplier']
    permission_denied_message = "You dont have permission to add supplier"
    form_class = CreateSupplierForm

    def get(self, request, *args, **kwargs):

        existing_suppliers = Supplier.objects.all().order_by('-pk')[:10]
        suppliers = []

        if existing_suppliers.count() > 0:

            num = 0

            for supplier in existing_suppliers:
                num = num + 1
                suppliers.append({
                    'num': num,
                    'name': supplier.name,
                    'supplier_code': supplier.supplier_code,
                    'primary_phone': supplier.primary_phone,
                    'email': supplier.email,
                    'pk': supplier.pk,
                })

        context = {
            'suppliers': suppliers,
            'form': self.form_class
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = CreateSupplierForm(data=request.POST)

        if form.is_valid():

            supplier = form.save(commit=False)
            supplier.supplier_code = supplier.name.replace(" ", "_").lower()
            supplier.save()

            messages.success(request, 'Success, supplier created', extra_tags='alert alert-success')

            return redirect(to='suppliers:create-supplier')

        else:

            existing_suppliers = Supplier.objects.all().order_by('-pk')[:10]
            suppliers = []

            if existing_suppliers.count() > 0:

                num = 0

                for supplier in suppliers:
                    suppliers.append({
                        'num': ++num,
                        'name': supplier.name,
                    })

            context = {
                'suppliers': suppliers
            }
            messages.error(request, 'Success, supplier created', extra_tags='alert alert-danger')

            return render(request, self.template_name, context=context)


class Home(PermissionRequiredMixin, TemplateView):
    template_name = 'suppliers/home.html'
    raise_exception = True
    permission_required = ['suppliers.view_supplier']
    permission_denied_message = "You dont have permission to view suppliers"

    def get(self, request, *args, **kwargs):

        existing_suppliers = Supplier.objects.all()
        suppliers = []

        if existing_suppliers.count() > 0:

            num = 0

            for supplier in existing_suppliers:
                num = num + 1
                suppliers.append({
                    'num': num,
                    'name': supplier.name,
                    'primary_phone': supplier.primary_phone,
                    'email': supplier.email,
                    'pk': supplier.pk,
                })

        context = {
            'suppliers': suppliers
        }

        return render(request, self.template_name, context=context)

