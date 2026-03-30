"""Reports App Admin"""
from django.contrib import admin


@admin.register()
class ReportAdmin(admin.ModelAdmin):
    """Report admin configuration."""
    list_display = ('report_id', 'report_type', 'severity', 'status', 'created_at')
    list_filter = ('report_type', 'severity', 'status')
    search_fields = ('report_id', 'reported_item_id')
    readonly_fields = ('created_at', 'updated_at')
