from django import forms
from costumers.models import Customers


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = '__all__'


class SendEmailForm(forms.Form):
    from_email = forms.EmailField()
    to_email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
