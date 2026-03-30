"""ML App Admin"""
from django.contrib import admin
from .models import MLModel, PredictionCache


@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    """Admin for ML models."""
    list_display = ['model_name', 'version', 'status', 'is_active', 'trained_at']
    list_filter = ['status', 'is_active', 'trained_at']
    search_fields = ['model_name', 'model_id']
    readonly_fields = ['model_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('model_id', 'model_name', 'model_type', 'version')
        }),
        ('Status', {
            'fields': ('status', 'is_active', 'error_message')
        }),
        ('Performance', {
            'fields': ('accuracy', 'metrics', 'training_samples')
        }),
        ('Configuration', {
            'fields': ('features_used', 'model_path')
        }),
        ('Timestamps', {
            'fields': ('trained_at', 'created_at', 'updated_at')
        }),
    )


@admin.register(PredictionCache)
class PredictionCacheAdmin(admin.ModelAdmin):
    """Admin for prediction cache."""
    list_display = ['cache_id', 'player1_id', 'player2_id', 'is_valid', 'predicted_at']
    list_filter = ['is_valid', 'expires_at']
    search_fields = ['player1_id', 'player2_id', 'cache_id']
    readonly_fields = ['cache_id', 'created_at']
