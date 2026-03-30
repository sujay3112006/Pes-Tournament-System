"""Matches App Admin"""
from django.contrib import admin


@admin.register()
class MatchAdmin(admin.ModelAdmin):
    """Match admin configuration."""
    list_display = ('match_id', 'team_a_name', 'team_b_name', 'status', 'match_date')
    list_filter = ('status', 'match_date')
    search_fields = ('match_id', 'team_a_name', 'team_b_name')
    readonly_fields = ('created_at', 'updated_at')
