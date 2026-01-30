from django.contrib import admin
from .models import Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'leader', 'get_members_count', 'total_points', 'created_at']
    search_fields = ['name', 'leader__username']
    filter_horizontal = ['members']
    ordering = ['-total_points']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_members_count(self, obj):
        return obj.members.count()
    get_members_count.short_description = 'Members'
