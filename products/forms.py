from django import forms
from products.models import Product


class UpdateProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['sku_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'rows': 1})
        self.fields['manufacturer'].widget.attrs.update({'class': 'form-control'})
        self.fields['supplier'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['buying_price'].widget.attrs.update({'class': 'form-control'})
        self.fields['retail_price'].widget.attrs.update({'class': 'form-control'})
        self.fields['wholesale_price'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Product
        exclude = ['created', 'product_image']


class CreateProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['sku_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'rows': 1})
        self.fields['manufacturer'].widget.attrs.update({'class': 'form-control'})
        self.fields['supplier'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Product
        exclude = ['created', 'product_image', 'quantity', 'buying_price', 'wholesale_price', 'retail_price']

