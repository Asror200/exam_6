from django import forms
from costumers.models import Customers


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = '__all__'


class SendEmailForm(forms.Form):
    from_email = forms.EmailField(required=False, label='optional')
    to_email = forms.EmailField(label='must')
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    def clean_from_email(self):
        from_email = self.cleaned_data.get('from_email')
        if not from_email:
            return 'berdiyevasror12@gmail.com'
        return from_email
