from django import forms
from product.models import Product
from product.models import ProductAttribute, Attribute, AttributeValue, Image


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'rating', 'discount', 'quantity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10, 'cols': 40}),
        }

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        if discount < 0 or discount > 100:
            raise forms.ValidationError("Discount must be between 0 and 100.")
        return discount


class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ['attribute', 'attribute_value']

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.product:
            instance.product = self.product
        if commit:
            instance.save()
        return instance


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
