from customers.models import Customer
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from customers.forms import CreateCustomerForm, UpdateCustomerForm


class Home(PermissionRequiredMixin, ListView):
    template_name = 'customers/home.html'
    permission_required = ['customers.view_customer']
    raise_exception = True
    permission_denied_message = "You dont have permission to view customers"
    context_object_name = 'customers'
    model = Customer

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)

        customers_list = Customer.objects.all().order_by('-pk')[:10]

        customers = []
        num = 0

        for customer in customers_list:

            num = num + 1

            customers.append({
                'num': num,
                'pk': customer.pk,
                'name': customer.name,
                'primary_phone': customer.primary_phone,
                'email': customer.email
            })

        context['customers'] = customers

        return context


class CreateCustomer(PermissionRequiredMixin, CreateView):
    permission_required = ['customers.add_customer']
    raise_exception = True
    permission_denied_message = "You dont have permission to add customers"
    model = Customer
    template_name = 'customers/create_customer.html'
    form_class = CreateCustomerForm

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        customers_list = Customer.objects.all().order_by('-pk')[:10]

        customers = []
        num = 0

        for customer in customers_list:
            num = num + 1

            customers.append({
                'num': num,
                'pk': customer.pk,
                'name': customer.name,
                'primary_phone': customer.primary_phone,
                'email': customer.email
            })

        context['customers'] = customers

        return context

    def get_success_url(self):

        messages.success(self.request, 'Success, new customer created', extra_tags='alert alert-success')

        return reverse_lazy('customers:create-customer')


class UpdateCustomer(PermissionRequiredMixin, UpdateView):
    permission_required = ['customers.change_customer']
    raise_exception = True
    permission_denied_message = "You dont have permission to change customers"
    template_name = 'customers/edit_customer.html'
    model = Customer
    form_class = UpdateCustomerForm

    def get_success_url(self):

        messages.success(self.request, 'Success, customer details updated', extra_tags='alert alert-success')

        return reverse_lazy(viewname='customers:update-customer', kwargs={'pk': self.kwargs['pk']})


class DeleteCustomer(PermissionRequiredMixin, DeleteView):
    permission_required = ['customers.delete_customer']
    raise_exception = True
    permission_denied_message = "You dont have permission to delete customers"
    model = Customer
    context_object_name = 'customer'

    def get_success_url(self):

        messages.success(self.request, 'Success, customer has been deleted', extra_tags='alert alert-success')

        return reverse_lazy(viewname='customers:home')
