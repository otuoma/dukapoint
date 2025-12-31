from django import forms
from suppliers.models import Supplier
from branches.models import Branch

class DeliveriesFiltersForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date_from'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_from'].widget.attrs.update({'placeholder': 'Date from'})
        self.fields['date_to'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_to'].widget.attrs.update({'placeholder': 'Date to'})
        self.fields['branch'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_from'].widget.attrs.update({'id': 'date_from'})
        self.fields['date_to'].widget.attrs.update({'id': 'date_to'})

    date_from = forms.DateField()
    date_to = forms.DateField()
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
    )


class DeliveryForm(forms.Form):
    product = forms.CharField()
    quantity = forms.IntegerField()
    buying_price = forms.FloatField(initial=0.0)
    retail_price = forms.FloatField(initial=0.0)
    wholesale_price = forms.FloatField(initial=0.0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['product'].widget.attrs.update({'class': 'form-control'})
        self.fields['product'].widget.attrs.update({'id': 'product_id'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'min': '1'})
        self.fields['buying_price'].widget.attrs.update({'class': 'form-control'})
        self.fields['buying_price'].widget.attrs.update({'min': '1'})
        self.fields['wholesale_price'].widget.attrs.update({'class': 'form-control'})
        self.fields['wholesale_price'].widget.attrs.update({'min': '1'})
        self.fields['retail_price'].widget.attrs.update({'class': 'form-control'})
        self.fields['retail_price'].widget.attrs.update({'min': '1'})


class SetSupplierForm(forms.Form):
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all())
    delivery_number = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['supplier'].widget.attrs.update({'class': 'form-control'})
        self.fields['delivery_number'].widget.attrs.update({'class': 'form-control'})


class ReceiveDeliveryForm(forms.Form):
    product = forms.CharField(max_length=150)
    quantity = forms.IntegerField(initial=1)
    buying_price = forms.FloatField(initial=0.0)
    retail_price = forms.FloatField(initial=0.0)
    wholesale_price = forms.FloatField(initial=0.0)
    received_from = forms.CharField(max_length=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['product'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['buying_price'].widget.attrs.update({'class': 'form-control'})
        self.fields['retail_price'].widget.attrs.update({'class': 'form-control'})
        self.fields['wholesale_price'].widget.attrs.update({'class': 'form-control'})
        self.fields['received_from'].widget.attrs.update({'class': 'form-control'})

