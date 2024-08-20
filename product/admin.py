from django.contrib import admin
from product.models import Image, Attribute, AttributeValue, ProductAttribute, Product

# Register your models here.
admin.site.register(Image)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')
    search_fields = ('name',)
    list_per_page = 10
    prepopulated_fields = {'slug': ('name',)}