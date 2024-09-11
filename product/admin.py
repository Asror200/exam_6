from django.contrib import admin
from django.utils.html import format_html

from product.models import Image, Attribute, AttributeValue, ProductAttribute, Product, Commit
from import_export.admin import ImportExportModelAdmin


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'created_at')
    search_fields = ('name',)
    list_per_page = 10
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Image)
class ImageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'get_image', 'product', 'created_at')
    search_fields = ('product',)
    list_per_page = 10

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="rounded-circle" style="width: 50px; height: 50px;" />',
                               obj.image.url)
        return format_html('<img src="{}" class="rounded-circle" style="width: 50px; height: auto;" />',
                           'https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-'
                           'background-user-symbol-vector-illustration.jpg?s=1024x1024&w=is&k=20&c=-mUWsTSENkugJ3qs5cov'
                           'paj-bhYpxXY-v9RDpzsw504=')

    get_image.short_description = 'Image'


@admin.register(Attribute)
class AttributeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'key_name', 'created_at')
    search_fields = ('key_name',)
    list_per_page = 10


@admin.register(AttributeValue)
class AttributeValueAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'value_name', 'created_at')
    search_fields = ('value_name',)
    list_per_page = 10


@admin.register(ProductAttribute)
class ProductAttributeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'product', 'attribute', 'attribute_value', 'created_at')
    search_fields = ('product',)
    list_per_page = 10


@admin.register(Commit)
class CommitAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'product', 'user_name', 'body', 'created_at')
    search_fields = ('created_at',)
    list_per_page = 10
