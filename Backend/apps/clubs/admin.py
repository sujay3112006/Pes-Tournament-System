"""Clubs App Admin"""
from django.contrib import admin


@admin.register()
class ClubAdmin(admin.ModelAdmin):
    """Club admin configuration."""
    list_display = ('name', 'owner_id', 'member_count', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('name', 'club_id', 'owner_id')
    readonly_fields = ('created_at', 'updated_at')
