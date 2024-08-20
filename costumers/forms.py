from django import forms
from costumers.models import Customers


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = '__all__'
