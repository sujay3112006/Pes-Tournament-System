"""Realtime App Admin"""
from django.contrib import admin

# Mongoengine models don't work with Django admin
# class NotificationAdmin(admin.ModelAdmin):
#     """Notification admin configuration."""
#     list_display = ('title', 'notification_type', 'user_id', 'is_read', 'created_at')
#     list_filter = ('notification_type', 'is_read', 'created_at')
#     search_fields = ('notification_id', 'user_id', 'title')
#     readonly_fields = ('created_at',)
