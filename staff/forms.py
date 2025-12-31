from django import forms
from staff.models import Staff


class ChangeBranchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['branch'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Staff
        fields = ['branch']


class UpdateStaffForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['national_id'].widget.attrs.update({'class': 'form-control'})
        self.fields['branch'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'national_id', 'branch', 'is_active', 'is_staff', 'is_superuser']


class CreateStaffForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['national_id'].widget.attrs.update({'class': 'form-control'})
        self.fields['branch'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'national_id', 'branch']

