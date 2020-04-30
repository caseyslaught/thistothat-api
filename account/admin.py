from django.contrib import admin


from account.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'uid', 'datetime_created']
    search_fields = ['email']
    list_filter = ['is_active']
    ordering = ['-datetime_created']

    readonly_fields = ['datetime_created', 'datetime_updated', 'uid']
    exclude = ['datetime_deleted', 'password']
