from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from branches.models import Branch
from branches.forms import CreateBranchForm, UpdateBranchForm
from django.contrib import messages
from suppliers.models import Supplier


class DeleteBranch(PermissionRequiredMixin, DeleteView):
    permission_required = ['branches.delete_branch']
    raise_exception = True
    permission_denied_message = "You dont have permission to delete branch"
    model = Branch

    def get_success_url(self):

        messages.success(self.request, 'Success, branch deleted.', extra_tags='alert alert-info')

        return reverse_lazy(viewname='branches:home')


class UpdateBranch(PermissionRequiredMixin, UpdateView):
    permission_required = ['branches.change_branch']
    raise_exception = True
    permission_denied_message = "You dont have permission to change branch"
    form_class = UpdateBranchForm
    template_name = 'branches/edit_branch.html'
    model = Branch

    def post(self, request, *args, **kwargs):

        branch = self.get_object()
        form = self.form_class(data=request.POST, instance=branch)

        if form.is_valid():

            # update supplier tbl
            supplier, created = Supplier.objects.update_or_create(name=branch.name)

            if not created:  # update supplier name

                supplier.name = form.cleaned_data['name']
                supplier.save()

            form.save()

            messages.success(self.request, 'Success, branch updated.', extra_tags='alert alert-success')

            return redirect(to=f"/branches/update-branch/{branch.pk}/")
        else:
            return render(request, self.template_name, context={'form': form, 'branch': branch})


class CreateBranch(PermissionRequiredMixin, CreateView):
    permission_required = ['branches.add_branch']
    raise_exception = True
    permission_denied_message = "You dont have permission to add branch"
    model = Branch
    template_name = 'branches/create_branch.html'
    form_class = CreateBranchForm

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['branches'] = Branch.objects.all().order_by('-pk')[:25]

        return context

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        branches = Branch.objects.all().order_by('-pk')[:25]

        if form.is_valid():

            branch = form.save(commit=False)
            branch.branch_code = branch.name.replace(" ", "_").lower()
            branch.save()

            # If this is first branch, automatically set current user's branch
            if branches.count() == 1:
                branch = branches.get()

                user = self.request.user
                user.branch_id = branch.pk
                user.save()

            # Auto-create branch as a supplier
            supplier = Supplier(
                name=form.cleaned_data['name'],
                supplier_code=form.cleaned_data['name'].replace(" ", "_"),
                primary_phone=form.cleaned_data['phone_contact'],
                address=form.cleaned_data['location']
            )
            supplier.save()

            messages.success(self.request, 'Success, branch has been created', extra_tags='alert alert-success')

            return redirect(to="/branches/create-branch/")

        else:

            messages.error(self.request, 'Failed, form validation failed', extra_tags='alert alert-danger')

        return render(request, self.template_name, context={'form': form})


class Home(PermissionRequiredMixin, TemplateView):
    template_name = 'branches/home.html'
    permission_required = ['branches.view_branch']
    permission_denied_message = "You dont have permission to view branches"
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

