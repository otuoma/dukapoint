from django import forms
from returns.models import ProductReturn


class AddReturnForm(forms.Form):
    product = forms.CharField()
    quantity = forms.IntegerField(initial=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['product'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})

    class Meta:

        fields = ["product", "quantity"]
