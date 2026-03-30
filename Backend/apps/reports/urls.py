"""Reports App URLs"""
from django.urls import path
from apps.reports.views import (
    CreateReportView,
    ReportDetailView,
    UserReportHistoryView,
    AdminReportListView,
    ReviewReportView,
    ResolveReportView,
    ReportStatsView,
    PendingReportsView,
)

urlpatterns = [
    # Report submission
    path('reports/create/', CreateReportView.as_view(), name='create_report'),
    path('reports/<str:report_id>/', ReportDetailView.as_view(), name='report_detail'),
    
    # User views
    path('my-reports/', UserReportHistoryView.as_view(), name='user_report_history'),
    
    # Admin views
    path('reports/admin/', AdminReportListView.as_view(), name='admin_report_list'),
    path('reports/pending/', PendingReportsView.as_view(), name='pending_reports'),
    path('reports/<str:report_id>/review/', ReviewReportView.as_view(), name='review_report'),
    path('reports/<str:report_id>/resolve/', ResolveReportView.as_view(), name='resolve_report'),
    
    # Stats
    path('reports/stats/', ReportStatsView.as_view(), name='report_stats'),
]
