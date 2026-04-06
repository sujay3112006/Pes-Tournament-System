"""Tournaments App Views"""
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.db.models import Q

from apps.tournaments.models import Tournament, TournamentPlayer
from apps.tournaments.serializers import (
    TournamentCreateSerializer,
    TournamentListSerializer,
    TournamentDetailSerializer,
    TournamentPlayerSerializer,
    JoinTournamentSerializer,
    TournamentUpdateSerializer,
)
from apps.users.models import User
import uuid
import logging

logger = logging.getLogger(__name__)


class CreateTournamentView(generics.CreateAPIView):
    """Create a new tournament."""
    serializer_class = TournamentCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        logger.info(f"Create tournament request: {request.data}")
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            logger.error(f"Tournament validation errors: {serializer.errors}")
            return Response(
                {
                    'message': 'Tournament validation failed',
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create tournament
        tournament_id = str(uuid.uuid4())
        tournament = Tournament(
            tournament_id=tournament_id,
            name=serializer.validated_data['name'],
            description=serializer.validated_data.get('description', ''),
            creator_id=request.user.user_id,
            format=serializer.validated_data['format'],
            max_players=serializer.validated_data['max_players'],
            start_date=serializer.validated_data['start_date'],
            end_date=serializer.validated_data['end_date'],
            location=serializer.validated_data.get('location', ''),
            rules=serializer.validated_data.get('rules', ''),
            prize_pool=serializer.validated_data.get('prize_pool', 0),
            is_public=serializer.validated_data['is_public'],
            status='draft',
        )
        tournament.save()
        
        # Auto-add creator as participant
        try:
            tournament_player = TournamentPlayer(
                tournament_player_id=str(uuid.uuid4()),
                tournament_id=tournament_id,
                user_id=request.user.user_id,
                username=request.user.username,
                status='active',
            )
            tournament_player.save()
            
            # Update tournament player count
            tournament.current_players = 1
            tournament.save()
            logger.info(f"Tournament created: {tournament_id} by {request.user.username}")
        except Exception as e:
            logger.error(f"Error adding creator to tournament: {str(e)}")
        
        return Response(
            {
                'message': 'Tournament created successfully',
                'tournament_id': tournament_id,
            },
            status=status.HTTP_201_CREATED
        )


class TournamentListView(generics.ListAPIView):
    """List all public tournaments or filtered by status."""
    serializer_class = TournamentListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Tournament.objects(is_public=True)
        
        # Filter by status
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset(status=status_param)
        
        # Filter by format
        format_param = self.request.query_params.get('format')
        if format_param:
            queryset = queryset(format=format_param)
        
        # Search by name
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset(name__icontains=search)
        
        # Order by creation date (newest first)
        return queryset.order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(queryset),
            'tournaments': serializer.data,
        })


class TournamentDetailView(generics.RetrieveAPIView):
    """Get tournament details including all players."""
    serializer_class = TournamentDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'tournament_id'
    lookup_url_kwarg = 'tournament_id'
    
    def retrieve(self, request, *args, **kwargs):
        tournament_id = kwargs.get('tournament_id')
        
        try:
            tournament = Tournament.objects.get(tournament_id=tournament_id)
            
            # Get all players in tournament
            players = TournamentPlayer.objects(tournament_id=tournament_id)
            
            tournament_data = TournamentDetailSerializer(tournament).data
            tournament_data['players'] = TournamentPlayerSerializer(players, many=True).data
            
            return Response(tournament_data)
        except Tournament.DoesNotExist:
            return Response(
                {'error': 'Tournament not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class JoinTournamentView(generics.GenericAPIView):
    """Join an existing tournament."""
    serializer_class = JoinTournamentSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, tournament_id, *args, **kwargs):
        try:
            tournament = Tournament.objects.get(tournament_id=tournament_id)
        except Tournament.DoesNotExist:
            return Response(
                {'error': 'Tournament not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if tournament is full
        if tournament.current_players >= tournament.max_players:
            return Response(
                {'error': 'Tournament is full'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user already joined
        existing_player = TournamentPlayer.objects(
            tournament_id=tournament_id,
            user_id=request.user.user_id
        ).first()
        
        if existing_player:
            return Response(
                {'error': 'You already joined this tournament'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check tournament status
        if tournament.status not in ['draft', 'registration']:
            return Response(
                {'error': 'Tournament is not accepting new players'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add player to tournament
        tournament_player = TournamentPlayer(
            tournament_player_id=str(uuid.uuid4()),
            tournament_id=tournament_id,
            user_id=request.user.user_id,
            username=request.user.username,
            status='active',
        )
        tournament_player.save()
        
        # Update tournament player count
        tournament.current_players += 1
        tournament.save()
        
        return Response(
            {
                'message': 'Successfully joined tournament',
                'tournament_id': tournament_id,
                'current_players': tournament.current_players,
                'max_players': tournament.max_players,
            },
            status=status.HTTP_200_OK
        )


class MyTournamentsView(generics.ListAPIView):
    """Get tournaments created by current user."""
    serializer_class = TournamentListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Tournament.objects(creator_id=self.request.user.user_id).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(queryset),
            'tournaments': serializer.data,
        })


class JoinedTournamentsView(generics.ListAPIView):
    """Get tournaments that current user joined."""
    serializer_class = TournamentDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        # Find all tournaments user joined
        user_tournaments = TournamentPlayer.objects(
            user_id=request.user.user_id
        ).distinct('tournament_id')
        
        tournament_ids = [tp.tournament_id for tp in user_tournaments]
        tournaments = Tournament.objects(tournament_id__in=tournament_ids).order_by('-created_at')
        
        serializer = self.get_serializer(tournaments, many=True)
        return Response({
            'count': len(tournaments),
            'tournaments': serializer.data,
        })


class LeaveTournamentView(generics.GenericAPIView):
    """Leave a tournament (if not started)."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, tournament_id, *args, **kwargs):
        try:
            tournament = Tournament.objects.get(tournament_id=tournament_id)
        except Tournament.DoesNotExist:
            return Response(
                {'error': 'Tournament not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Can't leave if tournament already started
        if tournament.status not in ['draft', 'registration']:
            return Response(
                {'error': 'Cannot leave an active or completed tournament'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if creator trying to leave
        if tournament.creator_id == request.user.user_id:
            return Response(
                {'error': 'Tournament creator cannot leave'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find and remove player
        tournament_player = TournamentPlayer.objects(
            tournament_id=tournament_id,
            user_id=request.user.user_id
        ).first()
        
        if not tournament_player:
            return Response(
                {'error': 'You are not in this tournament'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Delete player record
        tournament_player.delete()
        
        # Update tournament player count
        tournament.current_players = max(0, tournament.current_players - 1)
        tournament.save()
        
        return Response(
            {'message': 'Successfully left tournament'},
            status=status.HTTP_200_OK
        )
