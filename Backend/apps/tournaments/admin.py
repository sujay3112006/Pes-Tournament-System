"""Tournaments App Admin"""
from django.contrib import admin

# Mongoengine models don't work with Django admin
# class TournamentAdmin(admin.ModelAdmin):
#     """Tournament admin configuration."""
#     list_display = ('name', 'status', 'tournament_type', 'total_teams', 'created_at')
#     list_filter = ('status', 'tournament_type', 'is_public')
#     search_fields = ('name', 'creator_id')
#     readonly_fields = ('created_at', 'updated_at')
