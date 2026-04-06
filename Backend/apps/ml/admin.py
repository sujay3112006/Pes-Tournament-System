"""ML App Admin"""
from django.contrib import admin
# from .models import MLModel, PredictionCache

# Mongoengine models don't work with Django admin
# @admin.register(MLModel)
# class MLModelAdmin(admin.ModelAdmin):
#     """Admin for ML models."""
#     list_display = ['model_name', 'version', 'status', 'is_active', 'trained_at']
#     list_filter = ['status', 'is_active', 'trained_at']
#     search_fields = ['model_name', 'model_id']
#     readonly_fields = ['model_id', 'created_at', 'updated_at']
#     
#     fieldsets = (
#         ('Basic Info', {
#             'fields': ('model_id', 'model_name', 'model_type', 'version')
#         }),
#         ('Status', {
#             'fields': ('status', 'is_active', 'error_message')
#         }),
#         ('Performance', {
#             'fields': ('accuracy', 'metrics', 'training_samples')
#         }),
#         ('Configuration', {
#             'fields': ('features_used', 'model_path')\n        }),\n        ('Timestamps', {\n            'fields': ('trained_at', 'created_at', 'updated_at')\n        }),\n    )\n\n\n# @admin.register(PredictionCache)\n# class PredictionCacheAdmin(admin.ModelAdmin):\n#     """Admin for prediction cache.\"\"\"\n#     list_display = ['cache_id', 'player1_id', 'player2_id', 'is_valid', 'predicted_at']\n#     list_filter = ['is_valid', 'expires_at']\n#     search_fields = ['player1_id', 'player2_id', 'cache_id']\n#     readonly_fields = ['cache_id', 'created_at']
