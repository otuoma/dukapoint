from django import forms
from customers.models import Customer


class UpdateCustomerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['primary_phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['national_id'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['secondary_phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['additional_email'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['additional_address'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'rows': 1})
        self.fields['additional_address'].widget.attrs.update({'rows': 1})

    class Meta:
        model = Customer
        exclude = ['date_created']


class CreateCustomerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['primary_phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['national_id'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['secondary_phone'].widget.attrs.update({'class': 'form-control'})
        self.fields['additional_email'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['additional_address'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'rows': 1})
        self.fields['additional_address'].widget.attrs.update({'rows': 1})

    class Meta:
        model = Customer
        exclude = ['date_created']
