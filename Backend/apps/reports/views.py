"""Reports App Views"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from datetime import timedelta
from django.core.files.storage import default_storage

from apps.reports.models import Report
from apps.reports.serializers import (
    ReportListSerializer,
    ReportDetailSerializer,
    CreateReportSerializer,
    ReviewReportSerializer,
    ResolveReportSerializer,
    ReportStatsSerializer,
    ReportHistorySerializer,
    AdminReportListSerializer,
)
import uuid
import logging

logger = logging.getLogger(__name__)


class CreateReportView(generics.GenericAPIView):
    """Create a match report (anti-cheat)."""
    serializer_class = CreateReportSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user_id = request.user.user_id
            match_id = serializer.validated_data['match_id']
            
            # Check if match exists
            from apps.matches.models import Match
            try:
                match = Match.objects.get(match_id=match_id)
            except Match.DoesNotExist:
                return Response(
                    {'error': 'Match not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Check if user is involved in the match
            if user_id not in [match.player1_id, match.player2_id]:
                return Response(
                    {'error': 'You can only report matches you participated in'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Create report
            report = Report(
                report_id=str(uuid.uuid4()),
                match_id=match_id,
                reported_by_id=user_id,
                reported_by_username=request.user.username,
                reported_player_id=serializer.validated_data.get('reported_player_id'),
                reason=serializer.validated_data['reason'],
                description=serializer.validated_data.get('description', ''),
                severity=serializer.validated_data.get('severity', 'medium'),
            )
            
            # Handle proof files
            proof_files = serializer.validated_data.get('proof', [])
            if proof_files:
                proof_urls = []
                for proof_file in proof_files:
                    try:
                        # Generate unique filename
                        file_name = f"reports/{report.report_id}/{uuid.uuid4()}_{proof_file.name}"
                        # Save file
                        path = default_storage.save(file_name, proof_file)
                        # Get URL
                        proof_urls.append(default_storage.url(path))
                    except Exception as e:
                        logger.error(f"Error uploading proof: {str(e)}")
                
                if proof_urls:
                    report.proof_urls = proof_urls
            
            report.save()
            
            return Response(
                {
                    'message': 'Report submitted successfully',
                    'report_id': report.report_id,
                    'status': report.status,
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Error creating report: {str(e)}")
            return Response(
                {'error': 'Failed to create report'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ReportDetailView(generics.GenericAPIView):
    """Get report details."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, report_id, *args, **kwargs):
        try:
            report = Report.objects.get(report_id=report_id)
            
            # Check permissions: reporter, reported player, or admin
            user_id = request.user.user_id
            is_reporter = report.reported_by_id == user_id
            is_admin = request.user.is_staff  # Assuming is_staff for admins
            
            if not (is_reporter or is_admin):
                return Response(
                    {'error': 'Permission denied'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = ReportDetailSerializer(report)
            return Response(serializer.data)
        except Report.DoesNotExist:
            return Response(
                {'error': 'Report not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving report: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve report'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserReportHistoryView(generics.ListAPIView):
    """Get user's report history."""
    serializer_class = ReportHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.request.user.user_id
        queryset = Report.objects(reported_by_id=user_id).order_by('-created_at')
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(queryset),
            'reports': serializer.data,
        })


class AdminReportListView(generics.ListAPIView):
    """Get all reports for admin review."""
    serializer_class = AdminReportListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Admin check would be done in permissions in production
        status_filter = self.request.query_params.get('status')
        severity_filter = self.request.query_params.get('severity')
        
        queryset = Report.objects().order_by('-created_at')
        
        if status_filter:
            queryset = queryset(status=status_filter)
        if severity_filter:
            queryset = queryset(severity=severity_filter)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(queryset),
            'reports': serializer.data,
        })


class ReviewReportView(generics.GenericAPIView):
    """Admin review report (change status)."""
    serializer_class = ReviewReportSerializer
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, report_id, *args, **kwargs):
        try:
            report = Report.objects.get(report_id=report_id)
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Update status and admin info
            report.status = serializer.validated_data['status']
            report.reviewed_by = request.user.user_id
            report.updated_at = timezone.now()
            
            if 'action_taken' in serializer.validated_data:
                report.action_taken = serializer.validated_data['action_taken']
            
            if 'resolution_notes' in serializer.validated_data:
                report.resolution_notes = serializer.validated_data['resolution_notes']
            
            # Mark resolved if status is resolved/rejected/false_claim
            if report.status in ['resolved', 'rejected', 'false_claim']:
                report.resolved_at = timezone.now()
            
            report.save()
            
            return Response(
                {
                    'message': 'Report reviewed successfully',
                    'report_id': report.report_id,
                    'status': report.status,
                },
                status=status.HTTP_200_OK
            )
        except Report.DoesNotExist:
            return Response(
                {'error': 'Report not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error reviewing report: {str(e)}")
            return Response(
                {'error': 'Failed to review report'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ResolveReportView(generics.GenericAPIView):
    """Resolve a report with action."""
    serializer_class = ResolveReportSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, report_id, *args, **kwargs):
        try:
            report = Report.objects.get(report_id=report_id)
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Update report
            report.status = 'resolved'
            report.action_taken = serializer.validated_data['action_taken']
            report.resolution_notes = serializer.validated_data.get('resolution_notes', '')
            report.reviewed_by = request.user.user_id
            report.resolved_at = timezone.now()
            report.updated_at = timezone.now()
            report.save()
            
            # If action_taken is match_voided, void the match
            if serializer.validated_data['action_taken'] == 'match_voided':
                try:
                    from apps.matches.models import Match
                    match = Match.objects.get(match_id=report.match_id)
                    match.status = 'cancelled'
                    match.save()
                except:
                    pass
            
            return Response(
                {
                    'message': 'Report resolved successfully',
                    'report_id': report.report_id,
                    'action_taken': report.action_taken,
                },
                status=status.HTTP_200_OK
            )
        except Report.DoesNotExist:
            return Response(
                {'error': 'Report not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error resolving report: {str(e)}")
            return Response(
                {'error': 'Failed to resolve report'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ReportStatsView(generics.GenericAPIView):
    """Get report statistics."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            all_reports = Report.objects()
            
            total = len(all_reports)
            pending = len(Report.objects(status='pending'))
            under_review = len(Report.objects(status='under_review'))
            resolved = len(Report.objects(status='resolved'))
            rejected = len(Report.objects(status='rejected'))
            false_claims = len(Report.objects(status='false_claim'))
            
            # Calculate average resolution time
            resolved_reports = Report.objects(resolved_at__ne=None)
            if resolved_reports:
                total_time = sum([
                    (r.resolved_at - r.created_at).total_seconds()
                    for r in resolved_reports
                ])
                avg_time_hours = total_time / len(resolved_reports) / 3600
            else:
                avg_time_hours = 0
            
            return Response({
                'total_reports': total,
                'pending_reports': pending,
                'under_review': under_review,
                'resolved_reports': resolved,
                'rejected_reports': rejected,
                'false_claims': false_claims,
                'avg_resolution_time_hours': round(avg_time_hours, 2),
            })
        except Exception as e:
            logger.error(f"Error getting stats: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve statistics'},
                status=status.HTTP_400_BAD_REQUEST
            )


class PendingReportsView(generics.ListAPIView):
    """Get pending reports awaiting review."""
    serializer_class = AdminReportListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Report.objects(
            status__in=['pending', 'under_review']
        ).order_by('-severity', '-created_at')
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(queryset),
            'pending_reports': serializer.data,
        })
    
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
