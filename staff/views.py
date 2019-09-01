from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, DeleteView
from staff.models import Staff
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from staff.utils import get_all_perms, selected_perms
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from staff.forms import CreateStaffForm, UpdateStaffForm, ChangeBranchForm
from django.contrib.auth.models import Permission


class SetPermissions(PermissionRequiredMixin, FormView):
    template_name = 'staff/set_permissions.html'
    perms_list = get_all_perms()

    def has_permission(self):

        # only allow superuser to access this view
        if self.request.user.is_superuser:
            return True
        else:
            return False

    def get(self, request, *args, **kwargs):

        staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        staff_perms_query = staff.user_permissions.all()
        staff_perms = [staff_perm.codename for staff_perm in staff_perms_query]

        context = {
            'perms_list': self.perms_list,
            'staff_perms_query': staff_perms_query,
            'staff_perms': staff_perms,
            'staff': staff,
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        staff = get_object_or_404(Staff, pk=self.kwargs['pk'])

        perms_selected = selected_perms(form_data=request.POST)
        staff_perms_query = staff.user_permissions.all()
        staff_perms = [staff_perm.codename for staff_perm in staff_perms_query]

        # remove existing perm that is not selected
        for perm in staff_perms:
            if perm not in perms_selected:
                staff.user_permissions.remove(
                    Permission.objects.get(codename=perm)
                )

        # add new selected perm
        for perm in perms_selected:
            if perm not in staff_perms:
                staff.user_permissions.add(
                    Permission.objects.get(codename=perm)
                )

        messages.success(request, f"Success, updated permissions for {staff.last_name}", extra_tags="alert alert-success")

        return redirect(to=f"/staff/set-permissions/{staff.pk}/")


class ChangeBranch(PermissionRequiredMixin, FormView):
    """Change the branch a staff belongs to"""
    permission_required = ['staff.change_staff']
    raise_exception = True
    permission_denied_message = "You dont have permission to change staff"
    form_class = ChangeBranchForm
    template_name = "staff/change_branch.html"

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST, instance=request.user)

        if form.is_valid():

            form.save()

            messages.success(request, "Success, branch has been updated", extra_tags="alert alert-success")

        return redirect(to='/staff/update-staff/%s' % request.user.pk)


class UpdatePassword(PermissionRequiredMixin, FormView):
    permission_denied_message = "You dont have permission to change staff"
    raise_exception = True
    form_class = PasswordChangeForm

    def has_permission(self):

        staff = get_object_or_404(Staff, pk=self.kwargs['pk'])

        # Allow logged-in user or superuser to change password
        if staff.pk == self.request.user.pk or self.request.user.is_superuser:
            return True
        else:
            return False

    def post(self, request, *args, **kwargs):

        staff = get_object_or_404(Staff, pk=self.kwargs['pk'])

        form = self.form_class(user=staff, data=request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, 'Success, password updated', extra_tags='alert alert-success')
        else:
            messages.error(request, 'Failed, password NOT updated', extra_tags='alert alert-danger')

        return redirect(to='staff:update-staff', pk=self.kwargs['pk'])


class DeleteStaff(PermissionRequiredMixin, DeleteView):
    permission_required = ['staff.delete_staff']
    permission_denied_message = "You dont have permission to delete staff"
    raise_exception = True
    model = Staff

    def get_success_url(self):

        messages.success(self.request, 'Success, staff deleted', extra_tags='alert alert-info')

        return reverse_lazy('staff:home')


class UpdateStaff(PermissionRequiredMixin, FormView):
    template_name = 'staff/edit_staff.html'
    permission_required = ['staff.change_staff']
    permission_denied_message = "You dont have permission to change staff"
    raise_exception = True
    form_class = UpdateStaffForm
    password_form = PasswordChangeForm

    def post(self, request, *args, **kwargs):

        person = get_object_or_404(Staff, pk=self.kwargs['pk'])

        form = self.form_class(instance=person, data=request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, 'Success, staff details updated', extra_tags='alert alert-success')

            return redirect(to='staff:update-staff', pk=self.kwargs['pk'])
        else:

            context = {
                'form': self.form_class(data=request.POST, instance=person),
                'person': person,
                'password_form': self.password_form
            }

            messages.error(request, 'Failed, errors occurred.', extra_tags='alert alert-danger')

            return render(request, self.template_name, context=context)

    def get(self, request, *args, **kwargs):

        person = get_object_or_404(Staff, pk=self.kwargs['pk'])

        password_form = self.password_form(user=person)

        password_form.fields['old_password'].widget.attrs.pop("autofocus", None)

        context = {
            'form': self.form_class(instance=person),
            'person': person,
            'password_form': password_form
        }

        return render(request, self.template_name, context=context)


class CreateStaff(PermissionRequiredMixin, FormView):
    template_name = 'staff/create_staff.html'
    permission_required = ['staff.add_staff']
    permission_denied_message = "You dont have permission to add staff"
    form_class = CreateStaffForm

    def get(self, request, *args, **kwargs):

        staff = Staff.objects.all().order_by('-pk')[:10]
        persons = []

        if staff.count() > 0:

            num = 0

            for person in staff:

                num += 1

                persons.append({
                    'num': num,
                    'name': person.get_full_name(),
                    'email': person.email,
                    'phone_number': person.phone_number,
                    'pk': person.pk
                })

        context = {
            'form': self.form_class,
            'staff': persons
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():

            staff_obj = form.save(commit=False)
            staff_obj.is_staff = True

            # Set default password to phone_number
            staff_obj.set_password(
                raw_password=form.cleaned_data['phone_number']
            )

            staff_obj.save()

            messages.success(request, 'Success, staff created', extra_tags='alert alert-success')

            return redirect(to='staff:home')

        staff = Staff.objects.all().order_by('-pk')[:10]
        persons = []

        if staff.count() > 0:

            num = 0

            for person in staff:
                num += 1

                persons.append({
                    'num': num,
                    'name': person.get_full_name(),
                    'email': person.email,
                    'phone_number': person.phone_number,
                    'pk': person.pk
                })

        context = {
            'form': form,
            'staff': persons
        }

        messages.error(request, 'Errors occurred', extra_tags='alert alert-danger')

        return render(request, self.template_name, context=context)


class Logout(FormView):
    form_class = AuthenticationForm
    template_name = 'staff/login.html'

    def get(self, request, *args, **kwargs):

        logout(request)

        return redirect(to='/')


class Login(FormView):
    form_class = AuthenticationForm
    template_name = 'staff/login.html'

    def get(self, request, *args, **kwargs):

        if request.GET.get('next'):
            next_url = request.GET.get('next', '/staff/')
        else:
            next_url = '/staff bn/'

        context = {
            'next': next_url,
            'form': self.form_class
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        username = ''
        password = 'pa'

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            next_url = '/'

            return redirect(to=next_url)

        else:

            messages.error(request, 'Wrong username/password', extra_tags='alert alert-danger')

            form = self.form_class(initial={'username': username})

            return render(request, self.template_name, {'form': form})


class Home(PermissionRequiredMixin, TemplateView):
    template_name = 'staff/home.html'
    permission_required = ['staff.view_staff']
    permission_denied_message = "You dont have permission to view staff"
    raise_exception = True

    def get(self, request, *args, **kwargs):

        existing_staff = Staff.objects.all().order_by('-pk')
        staff = []

        if existing_staff.count() > 0:

            num = 0

            for person in existing_staff:
                num = num + 1
                staff.append({
                    'num': num,
                    'name': person.get_full_name(),
                    'phone_number': person.phone_number,
                    'email': person.email,
                    'branch': person.branch,
                    'pk': person.pk,
                })
        else:

            staff = None

        context = {
            'staff': staff
        }

        return render(request, self.template_name, context=context)
