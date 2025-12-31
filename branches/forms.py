from django import forms
from branches.models import Branch


class UpdateBranchForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['location'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_contact'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Branch
        fields = ['name', 'location', 'email', 'phone_contact']


class CreateBranchForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        # self.fields['branch_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['location'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_contact'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Branch
        fields = ['name', 'location', 'email', 'phone_contact']

