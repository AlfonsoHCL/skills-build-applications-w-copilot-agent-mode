from django.contrib import admin
from .models import Achievement, UserAchievement

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'requirement_type', 'requirement_value', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['created_at']
    readonly_fields = ['created_at']

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'earned_at']
    search_fields = ['user__username', 'achievement__name']
    list_filter = ['earned_at']
    readonly_fields = ['earned_at']
