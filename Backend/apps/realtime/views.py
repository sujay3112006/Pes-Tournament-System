"""Realtime App Views"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.realtime.models import Notification
from apps.realtime.serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """Notification ViewSet."""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects(user_id=str(self.request.user.id))
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications."""
        notifications = Notification.objects(user_id=str(request.user.id), is_read=False)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark notification as read."""
        try:
            notification = Notification.objects.get(notification_id=pk)
            notification.is_read = True
            notification.save()
            return Response({'message': 'Marked as read'})
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=404)
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read."""
        Notification.objects(user_id=str(request.user.id), is_read=False).update(is_read=True)
        return Response({'message': 'All notifications marked as read'})
