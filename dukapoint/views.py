from django.shortcuts import render
from django.views.generic import TemplateView
from suppliers.models import Supplier
from django.contrib.auth.mixins import PermissionRequiredMixin


class Home(PermissionRequiredMixin, TemplateView):

    template_name = 'home.html'
    permission_denied_message = "You dont have permission to access page"

    def has_permission(self):

        if self.request.user.is_staff or self.request.user.is_superuser:

            return True
        else:
            return False
