"""Matches App Views"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.matches.models import Match, MatchEvent
from apps.matches.serializers import MatchSerializer, MatchEventSerializer


class MatchViewSet(viewsets.ModelViewSet):
    """Match ViewSet."""
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Match.objects()
    
    @action(detail=True, methods=['post'])
    def update_score(self, request, pk=None):
        """Update match score."""
        match_id = pk
        team_a_score = request.data.get('team_a_score')
        team_b_score = request.data.get('team_b_score')
        
        try:
            match = Match.objects.get(match_id=match_id)
            match.team_a_score = team_a_score
            match.team_b_score = team_b_score
            
            if team_a_score > team_b_score:
                match.winner_id = match.team_a_id
            elif team_b_score > team_a_score:
                match.winner_id = match.team_b_id
            
            match.save()
            return Response({'message': 'Score updated successfully'})
        except Match.DoesNotExist:
            return Response({'error': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)


class MatchEventViewSet(viewsets.ModelViewSet):
    """Match Event ViewSet."""
    serializer_class = MatchEventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return MatchEvent.objects()
