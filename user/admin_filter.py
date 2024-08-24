from django.contrib import admin
import datetime


class JoinedDateFilter(admin.SimpleListFilter):
    """ This function is used to filter objects by joined date """
    title = 'filter'
    parameter_name = 'joined_date'

    def lookups(self, request, model_admin):
        return [
            ('super_user', 'Super user'),
            ('is_active', 'Is active'),
            ('is_staff', 'Is staff'),

        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'super_user':
            return queryset.filter(is_superuser=True)
        if value == 'is_active':
            return queryset.filter(is_active=True)
        if value == 'is_staff':
            return queryset.filter(is_staff=True)
        return queryset
