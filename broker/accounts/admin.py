from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Account, UserProfile


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'last_login', 'date_joined', 'confirm_email')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined', )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'country')


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
