from django import forms
from costumers.models import Customers, User


class SingUpForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'image')

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords must match')
        return password

    def save(self, commit=True):
        user = super(SingUpForm, self).save(commit=False)
        user.set_password(self.data['password'])
        user.is_superuser = True
        user.is_staff = True

        if commit:
            user.save()

        return user


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = '__all__'
