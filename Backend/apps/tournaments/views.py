"""Tournaments App Views"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.tournaments.models import Tournament, TournamentTeam
from apps.tournaments.serializers import TournamentSerializer, TournamentTeamSerializer


class TournamentViewSet(viewsets.ModelViewSet):
    """Tournament ViewSet."""
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Tournament.objects()
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a tournament."""
        tournament_id = pk
        team_data = request.data
        
        try:
            tournament = Tournament.objects.get(tournament_id=tournament_id)
            
            if tournament.status != 'active':
                return Response(
                    {'error': 'Tournament is not active'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            TournamentTeam.objects.create(
                tournament_id=tournament_id,
                team_id=team_data.get('team_id'),
                team_name=team_data.get('team_name'),
                captain_id=str(request.user.id),
                members=team_data.get('members', [])
            )
            
            return Response({'message': 'Successfully joined tournament'})
        except Tournament.DoesNotExist:
            return Response(
                {'error': 'Tournament not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def my_tournaments(self, request):
        """Get tournaments created by the user."""
        tournaments = Tournament.objects(creator_id=str(request.user.id))
        serializer = TournamentSerializer(tournaments, many=True)
        return Response(serializer.data)


class TournamentTeamViewSet(viewsets.ModelViewSet):
    """Tournament Team ViewSet."""
    serializer_class = TournamentTeamSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TournamentTeam.objects()
