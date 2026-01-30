from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('bio', 'avatar', 'role', 'points')}),
    )
    list_display = ['username', 'first_name', 'last_name', 'email', 'role', 'points', 'created_at']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['-points']

admin.site.register(User, CustomUserAdmin)
