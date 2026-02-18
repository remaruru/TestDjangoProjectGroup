from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_customer', 'is_seller')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_customer', 'is_seller')}),
    )
    list_display = UserAdmin.list_display + ('is_customer', 'is_seller')

admin.site.register(User, CustomUserAdmin)
