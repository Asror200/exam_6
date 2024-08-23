from django.contrib import admin
from django.utils.html import format_html
from costumers.models import Customers
from costumers.admin_filter import JoinedDateFilter
from django.contrib.auth.models import Group
from user.models import User
# Register your models here.
admin.site.unregister(Group)
admin.site.register(User)


@admin.register(Customers)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'get_image', 'joined')
    search_fields = ('first_name', 'email')
    prepopulated_fields = {'slug': ('email',)}
    list_filter = [JoinedDateFilter]

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="rounded-circle" style="width: 50px; height: 50px;" />', obj.image.url)
        return format_html('<img src="{}" class="rounded-circle" style="width: 50px; height: auto;" />',
                           'https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-'
                           'background-user-symbol-vector-illustration.jpg?s=1024x1024&w=is&k=20&c=-mUWsTSENkugJ3qs5cov'
                           'paj-bhYpxXY-v9RDpzsw504=')

    get_image.short_description = 'Image'

