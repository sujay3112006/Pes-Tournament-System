"""Matches App Views"""
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from django.core.files.storage import default_storage

from apps.matches.models import Match, MatchEvent
from apps.matches.serializers import (
    MatchListSerializer,
    MatchDetailSerializer,
    SubmitMatchResultSerializer,
    UpdateMatchResultSerializer,
    MatchEventSerializer,
    MatchStatsSerializer,
)
from apps.tournaments.models import TournamentPlayer
import uuid
import logging

logger = logging.getLogger(__name__)


class TournamentMatchesView(generics.ListAPIView):
    """Get all matches in a tournament."""
    serializer_class = MatchListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        tournament_id = self.kwargs.get('tournament_id')
        queryset = Match.objects(tournament_id=tournament_id)
        
        # Filter by status
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset(status=status_param)
        
        return queryset.order_by('match_date')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(queryset),
            'matches': serializer.data,
        })


class MatchDetailView(generics.RetrieveAPIView):
    """Get match details with all events."""
    serializer_class = MatchDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'match_id'
    lookup_url_kwarg = 'match_id'
    
    def retrieve(self, request, *args, **kwargs):
        match_id = kwargs.get('match_id')
        
        try:
            match = Match.objects.get(match_id=match_id)
            events = MatchEvent.objects(match_id=match_id).order_by('created_at')
            
            data = MatchDetailSerializer(match).data
            data['events'] = MatchEventSerializer(events, many=True).data
            
            return Response(data)
        except Match.DoesNotExist:
            return Response(
                {'error': 'Match not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class SubmitMatchResultView(generics.GenericAPIView):
    """Submit match result with proof."""
    serializer_class = SubmitMatchResultSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, match_id, *args, **kwargs):
        try:
            match = Match.objects.get(match_id=match_id)
        except Match.DoesNotExist:
            return Response(
                {'error': 'Match not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verify user is one of the players
        user_id = request.user.user_id
        if user_id not in [match.player1_id, match.player2_id]:
            return Response(
                {'error': 'Only players in this match can submit results'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check match status
        if match.status == 'completed':
            return Response(
                {'error': 'Match already completed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Update match score
        match.score = {
            'player1': serializer.validated_data['player1_score'],
            'player2': serializer.validated_data['player2_score'],
        }
        
        # Determine winner
        if serializer.validated_data['player1_score'] > serializer.validated_data['player2_score']:
            match.winner_id = match.player1_id
        elif serializer.validated_data['player2_score'] > serializer.validated_data['player1_score']:
            match.winner_id = match.player2_id
        # If draw, winner_id remains None
        
        # Update other fields
        match.status = 'completed'
        match.location = serializer.validated_data.get('location', match.location)
        match.duration = serializer.validated_data.get('duration', match.duration)
        
        # Handle proof upload
        proof_file = serializer.validated_data.get('proof')
        if proof_file:
            try:
                # Generate unique filename
                file_name = f"matches/{match_id}/{uuid.uuid4()}_{proof_file.name}"
                # Save file
                path = default_storage.save(file_name, proof_file)
                # Get URL
                match.proof_url = default_storage.url(path)
            except Exception as e:
                logger.error(f"Error uploading proof: {str(e)}")
                return Response(
                    {'error': 'Failed to upload proof'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        match.updated_at = timezone.now()
        match.save()
        
        # Update winner stats (if applicable)
        if match.winner_id:
            try:
                from apps.users.models import UserStatistics
                winner_stats = UserStatistics.objects.get(user_id=match.winner_id)
                winner_stats.match_wins += 1
                winner_stats.total_matches += 1
                winner_stats.save()
                
                loser_id = match.player2_id if match.player1_id == match.winner_id else match.player1_id
                loser_stats = UserStatistics.objects.get(user_id=loser_id)
                loser_stats.match_losses += 1
                loser_stats.total_matches += 1
                loser_stats.save()
            except Exception as e:
                logger.error(f"Error updating user statistics: {str(e)}")
        
        return Response(
            {
                'message': 'Match result submitted successfully',
                'match_id': match_id,
                'winner_id': match.winner_id,
                'status': match.status,
            },
            status=status.HTTP_200_OK
        )


class UpdateMatchResultView(generics.GenericAPIView):
    """Update existing match result (admin/tournament creator)."""
    serializer_class = UpdateMatchResultSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def put(self, request, match_id, *args, **kwargs):
        try:
            match = Match.objects.get(match_id=match_id)
        except Match.DoesNotExist:
            return Response(
                {'error': 'Match not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verify user is match creator or admin (for now, just allow match players)
        user_id = request.user.user_id
        if user_id not in [match.player1_id, match.player2_id]:
            return Response(
                {'error': 'Only match players can update results'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Update score if provided
        if 'player1_score' in serializer.validated_data or 'player2_score' in serializer.validated_data:
            player1_score = serializer.validated_data.get('player1_score', match.score.get('player1', 0))
            player2_score = serializer.validated_data.get('player2_score', match.score.get('player2', 0))
            
            match.score = {
                'player1': player1_score,
                'player2': player2_score,
            }
            
            # Determine winner
            if player1_score > player2_score:
                match.winner_id = match.player1_id
            elif player2_score > player1_score:
                match.winner_id = match.player2_id
            else:
                match.winner_id = None
        
        # Update other fields
        if 'status' in serializer.validated_data:
            match.status = serializer.validated_data['status']
        if 'location' in serializer.validated_data:
            match.location = serializer.validated_data['location']
        if 'duration' in serializer.validated_data:
            match.duration = serializer.validated_data['duration']
        
        # Handle proof upload
        proof_file = serializer.validated_data.get('proof')
        if proof_file:
            try:
                # Delete old proof if exists
                if match.proof_url:
                    try:
                        default_storage.delete(match.proof_url)
                    except Exception:
                        pass
                
                # Save new file
                file_name = f"matches/{match_id}/{uuid.uuid4()}_{proof_file.name}"
                path = default_storage.save(file_name, proof_file)
                match.proof_url = default_storage.url(path)
            except Exception as e:
                logger.error(f"Error uploading proof: {str(e)}")
                return Response(
                    {'error': 'Failed to upload proof'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        match.updated_at = timezone.now()
        match.save()
        
        return Response(
            {
                'message': 'Match result updated successfully',
                'match_id': match_id,
                'winner_id': match.winner_id,
                'status': match.status,
            },
            status=status.HTTP_200_OK
        )


class UserMatchStatsView(generics.GenericAPIView):
    """Get match statistics for a user."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id=None, *args, **kwargs):
        if user_id is None:
            user_id = request.user.user_id
        
        try:
            from apps.users.models import User, UserStatistics
            user = User.objects.get(user_id=user_id)
            stats = UserStatistics.objects.get(user_id=user_id)
            
            return Response({
                'user_id': user_id,
                'username': user.username,
                'total_matches': stats.total_matches,
                'wins': stats.match_wins,
                'losses': stats.match_losses,
                'draws': stats.match_draws,
                'win_rate': stats.win_rate,
                'goals_scored': stats.goals_scored,
            })
        except Exception as e:
            return Response(
                {'error': 'Statistics not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class PlayerMatchesView(generics.ListAPIView):
    """Get all matches for a specific player."""
    serializer_class = MatchListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        # Find all matches where user is player1 or player2
        from mongoengine import Q
        matches = Match.objects(
            Q(player1_id=user_id) | Q(player2_id=user_id)
        ).order_by('-match_date')
        return matches
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(queryset),
            'matches': serializer.data,
        })
