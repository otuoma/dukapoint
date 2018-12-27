from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from branches.models import Branch
from branches.forms import CreateBranchForm, UpdateBranchForm
from django.contrib import messages


class DeleteBranch(PermissionRequiredMixin, DeleteView):
    permission_required = ['branches.delete_branch']
    raise_exception = True
    model = Branch

    def get_success_url(self):

        messages.success(self.request, 'Success, branch deleted.', extra_tags='alert alert-info')

        return reverse_lazy(viewname='branches:home')


class UpdateBranch(PermissionRequiredMixin, UpdateView):
    permission_required = ['branches.change_branch']
    raise_exception = True
    form_class = UpdateBranchForm
    template_name = 'branches/edit_branch.html'
    model = Branch

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['branches'] = Branch.objects.all().order_by('-pk')

        return context

    def get_success_url(self):

        messages.success(self.request, 'Success, branch updated.', extra_tags='alert alert-success')

        return reverse_lazy(viewname='branches:update-branch', kwargs={'pk': self.kwargs['pk']})


class CreateBranch(PermissionRequiredMixin, CreateView):
    permission_required = ['branches.add_branch']
    raise_exception = True
    model = Branch
    template_name = 'branches/create_branch.html'
    form_class = CreateBranchForm

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['branches'] = Branch.objects.all().order_by('-pk')[:25]

        return context

    def get_success_url(self):

        messages.success(self.request, 'Success, branch has been created', extra_tags='alert alert-success')

        return reverse_lazy(viewname='branches:create-branch')


class Home(PermissionRequiredMixin, TemplateView):
    template_name = 'branches/home.html'
    permission_required = ['branches.add_branch']
    raise_exception = True

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        branches = Branch.objects.all().order_by('-pk')
        num = 0
        context['branches'] = []

        for branch in branches:

            num += 1

            context['branches'].append({
                'pk': branch.pk,
                'num': num,
                'name': branch.name,
                'branch_code': branch.branch_code,
                'location': branch.location,
                'phone_contact': branch.phone_contact,
                'email': branch.email,
                'created': branch.created,
            })

        return context

