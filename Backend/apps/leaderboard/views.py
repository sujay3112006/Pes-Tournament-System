"""Leaderboard App Views"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.leaderboard.models import Leaderboard, LeaderboardEntry
from apps.leaderboard.serializers import LeaderboardEntrySerializer


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """Leaderboard ViewSet."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Leaderboard.objects()
    
    @action(detail=True, methods=['get'])
    def entries(self, request, pk=None):
        """Get leaderboard entries."""
        leaderboard_id = pk
        entries = LeaderboardEntry.objects(leaderboard_id=leaderboard_id).order_by('rank')
        serializer = LeaderboardEntrySerializer(entries, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def tournament(self, request):
        """Get leaderboard for tournament."""
        tournament_id = request.query_params.get('tournament_id')
        try:
            leaderboard = Leaderboard.objects.get(tournament_id=tournament_id)
            entries = LeaderboardEntry.objects(leaderboard_id=str(leaderboard.id)).order_by('rank')
            serializer = LeaderboardEntrySerializer(entries, many=True)
            return Response(serializer.data)
        except Leaderboard.DoesNotExist:
            return Response({'error': 'Leaderboard not found'}, status=404)
