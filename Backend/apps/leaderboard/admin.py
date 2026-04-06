"""Leaderboard App Admin"""
from django.contrib import admin

# Mongoengine models don't work with Django admin
# class LeaderboardAdmin(admin.ModelAdmin):
#     """Leaderboard admin configuration."""
#     list_display = ('leaderboard_id', 'tournament_id', 'created_at')
#     search_fields = ('tournament_id',)
#     readonly_fields = ('created_at', 'updated_at')
