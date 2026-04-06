"""Missions App Admin"""
from django.contrib import admin

# Mongoengine models don't work with Django admin
# class MissionAdmin(admin.ModelAdmin):
#     """Mission admin configuration."""
#     list_display = ('title', 'mission_type', 'difficulty', 'reward_points', 'status')
#     list_filter = ('mission_type', 'difficulty', 'status')
#     search_fields = ('title', 'mission_id')
#     readonly_fields = ('created_at',)
