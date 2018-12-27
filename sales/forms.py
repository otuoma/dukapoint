from django import forms
from branches.models import Branch


class SalesFiltersForm(forms.Form):

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
        # required=False
    )


class SaleForm(forms.Form):

    confirm_sale = forms.CharField(max_length=150)


class AddToCartForm(forms.Form):

    product_name = forms.CharField(max_length=150)
    unit_price = forms.FloatField(initial=0.0)
    quantity = forms.IntegerField(initial=1)
    total = forms.FloatField(initial=1.0)
    product_id = forms.IntegerField()
