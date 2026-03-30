"""Reports App Views"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.reports.models import Report
from apps.reports.serializers import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    """Report ViewSet."""
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Report.objects()
    
    def create(self, request, *args, **kwargs):
        """Create a new report."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create report with current user as reporter
        report_data = serializer.validated_data
        report_data['reported_by_id'] = str(request.user.id)
        
        Report.objects.create(**report_data)
        
        return Response(
            {'message': 'Report submitted successfully'},
            status=status.HTTP_201_CREATED
        )
