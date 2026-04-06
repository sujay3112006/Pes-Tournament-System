"""Leaderboard App Views"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone

from apps.leaderboard.models import Leaderboard, LeaderboardEntry
from apps.leaderboard.serializers import (
    LeaderboardSerializer,
    LeaderboardEntrySerializer,
    RankingListSerializer,
    UpdateMatchResultSerializer,
    PlayerLeaderboardStatsSerializer,
    LeaderboardComparisonSerializer,
    TopPlayersSerializer,
)
import uuid
import logging

logger = logging.getLogger(__name__)


class TournamentLeaderboardView(generics.RetrieveAPIView):
    """Get tournament leaderboard/rankings."""
    permission_classes = [AllowAny]
    
    def retrieve(self, request, tournament_id, *args, **kwargs):
        try:
            # Get or create leaderboard
            leaderboard, created = Leaderboard.objects.get_or_create(
                tournament_id=tournament_id
            )
            
            # Get all entries sorted by rank
            entries = LeaderboardEntry.objects(
                tournament_id=tournament_id
            ).order_by('rank')
            
            serializer = RankingListSerializer(entries, many=True)
            
            return Response({
                'leaderboard_id': leaderboard.leaderboard_id,
                'tournament_id': tournament_id,
                'total_entries': len(entries),
                'rankings': serializer.data,
                'updated_at': leaderboard.updated_at,
            })
        except Exception as e:
            logger.error(f"Error retrieving leaderboard: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve leaderboard'},
                status=status.HTTP_400_BAD_REQUEST
            )


class TopPlayersView(generics.ListAPIView):
    """Get top N players in tournament."""
    serializer_class = TopPlayersSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, tournament_id, *args, **kwargs):
        limit = int(request.query_params.get('limit', 10))
        limit = min(limit, 100)  # Max 100
        
        entries = LeaderboardEntry.objects(
            tournament_id=tournament_id
        ).order_by('rank')[:limit]
        
        serializer = self.get_serializer(entries, many=True)
        
        return Response({
            'tournament_id': tournament_id,
            'limit': limit,
            'count': len(entries),
            'top_players': serializer.data,
        })


class PlayerLeaderboardStatsView(generics.GenericAPIView):
    """Get player's leaderboard statistics in a tournament."""
    permission_classes = [AllowAny]
    
    def get(self, request, tournament_id, user_id, *args, **kwargs):
        try:
            entry = LeaderboardEntry.objects.get(
                tournament_id=tournament_id,
                user_id=user_id
            )
            
            serializer = PlayerLeaderboardStatsSerializer(entry)
            return Response(serializer.data)
        except LeaderboardEntry.DoesNotExist:
            return Response(
                {'error': 'Player not found in leaderboard'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving player stats: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve player statistics'},
                status=status.HTTP_400_BAD_REQUEST
            )


class PlayerRankComparisonView(generics.GenericAPIView):
    """Compare player's position with leaderboard context."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, tournament_id, *args, **kwargs):
        user_id = request.user.user_id
        
        try:
            # Get player entry
            player_entry = LeaderboardEntry.objects.get(
                tournament_id=tournament_id,
                user_id=user_id
            )
            
            # Get top player (rank 1)
            top_player = LeaderboardEntry.objects(
                tournament_id=tournament_id,
                rank=1
            ).first()
            
            # Calculate points to next rank
            next_rank = player_entry.rank - 1 if player_entry.rank > 1 else None
            points_to_next = None
            
            if next_rank:
                next_entry = LeaderboardEntry.objects(
                    tournament_id=tournament_id,
                    rank=next_rank
                ).first()
                if next_entry:
                    points_to_next = next_entry.points - player_entry.points
            
            # Calculate percentage to first
            percentage_to_first = 0
            if top_player and top_player.user_id != user_id:
                if top_player.points > 0:
                    percentage_to_first = round(
                        (player_entry.points / top_player.points) * 100, 2
                    )
            elif top_player and top_player.user_id == user_id:
                percentage_to_first = 100
            
            return Response({
                'user_id': user_id,
                'username': player_entry.username,
                'rank': player_entry.rank,
                'points': player_entry.points,
                'total_players': LeaderboardEntry.objects(tournament_id=tournament_id).count(),
                'points_to_next': points_to_next,
                'percentage_to_first': percentage_to_first,
                'is_first': player_entry.rank == 1,
            })
        except LeaderboardEntry.DoesNotExist:
            return Response(
                {'error': 'Player not in leaderboard'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error comparing player rank: {str(e)}")
            return Response(
                {'error': 'Failed to compare rank'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UpdateMatchResultView(generics.GenericAPIView):
    """Update player points after match result."""
    serializer_class = UpdateMatchResultSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        tournament_id = serializer.validated_data['tournament_id']
        player1_id = serializer.validated_data['player1_id']
        player2_id = serializer.validated_data['player2_id']
        player1_score = serializer.validated_data['player1_score']
        player2_score = serializer.validated_data['player2_score']
        winner_id = serializer.validated_data.get('winner_id')
        
        try:
            # Get or create leaderboard
            leaderboard, _ = Leaderboard.objects.get_or_create(
                tournament_id=tournament_id
            )
            
            # Get or create entries for both players
            player1_entry, created1 = LeaderboardEntry.objects.get_or_create(
                tournament_id=tournament_id,
                user_id=player1_id,
                defaults={'username': '', 'rank': 999}  # Will be updated
            )
            
            player2_entry, created2 = LeaderboardEntry.objects.get_or_create(
                tournament_id=tournament_id,
                user_id=player2_id,
                defaults={'username': '', 'rank': 999}  # Will be updated
            )
            
            # Update match count and goal difference
            player1_entry.matches_played += 1
            player2_entry.matches_played += 1
            player1_entry.goal_difference += (player1_score - player2_score)
            player2_entry.goal_difference += (player2_score - player1_score)
            
            # Determine match result and award points
            # Win = 3 points, Draw = 1 point, Loss = 0 points
            if winner_id == player1_id:
                # Player 1 wins
                player1_entry.wins += 1
                player2_entry.losses += 1
                player1_entry.points += 3
            elif winner_id == player2_id:
                # Player 2 wins
                player2_entry.wins += 1
                player1_entry.losses += 1
                player2_entry.points += 3
            else:
                # Draw
                player1_entry.draws += 1
                player2_entry.draws += 1
                player1_entry.points += 1
                player2_entry.points += 1
            
            player1_entry.updated_at = timezone.now()
            player2_entry.updated_at = timezone.now()
            
            player1_entry.save()
            player2_entry.save()
            
            # Recalculate all rankings
            self._recalculate_rankings(tournament_id)
            
            # Update leaderboard timestamp
            leaderboard.updated_at = timezone.now()
            leaderboard.save()
            
            return Response(
                {
                    'message': 'Match result updated',
                    'player1_points': player1_entry.points,
                    'player1_rank': player1_entry.rank,
                    'player2_points': player2_entry.points,
                    'player2_rank': player2_entry.rank,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error updating match result: {str(e)}")
            return Response(
                {'error': 'Failed to update match result'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def _recalculate_rankings(self, tournament_id):
        """Recalculate rankings based on points (descending)."""
        try:
            # Get all entries sorted by points (descending), then by goal difference
            entries = LeaderboardEntry.objects(
                tournament_id=tournament_id
            ).order_by('-points', '-goal_difference')
            
            # Update ranks
            for rank, entry in enumerate(entries, 1):
                entry.rank = rank
                entry.save()
        except Exception as e:
            logger.error(f"Error recalculating rankings: {str(e)}")


class RankedPlayerListView(generics.ListAPIView):
    """Get all players in tournament ranked."""
    serializer_class = RankingListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        tournament_id = self.kwargs.get('tournament_id')
        queryset = LeaderboardEntry.objects(
            tournament_id=tournament_id
        ).order_by('rank')
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(queryset),
            'rankings': serializer.data,
        })


# ── Global Leaderboard Views (Not Tournament-Specific) ────────────────────────

class GlobalTopPlayersView(generics.ListAPIView):
    """Get top N players across all tournaments."""
    serializer_class = TopPlayersSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        limit = int(request.query_params.get('limit', 10))
        limit = min(limit, 100)  # Max 100
        
        # Get unique players and their total points across all tournaments
        from django.db.models import Sum
        try:
            # For MongoDB, we need a different approach
            # Get all entries and aggregate by user
            all_entries = LeaderboardEntry.objects.all()
            
            # Group by user_id and sum points
            user_points = {}
            for entry in all_entries:
                if entry.user_id not in user_points:
                    user_points[entry.user_id] = {
                        'user_id': entry.user_id,
                        'username': entry.username,
                        'points': 0,
                        'matches_played': 0,
                        'wins': 0,
                    }
                user_points[entry.user_id]['points'] += entry.points if entry.points else 0
            
            # Sort by points (descending) and take top N
            sorted_players = sorted(
                user_points.values(),
                key=lambda x: x['points'],
                reverse=True
            )[:limit]
            
            return Response({
                'limit': limit,
                'count': len(sorted_players),
                'results': sorted_players,
            })
        except Exception as e:
            logger.error(f"Error retrieving global top players: {str(e)}")
            return Response(
                {'results': []},
                status=status.HTTP_200_OK
            )


class GlobalRankingsView(generics.ListAPIView):
    """Get global rankings across all tournaments."""
    serializer_class = RankingListSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        limit = int(request.query_params.get('limit', 20))
        limit = min(limit, 100)  # Max 100
        
        try:
            # Get all entries and aggregate by user
            all_entries = LeaderboardEntry.objects.all()
            
            # Group by user_id and sum points
            user_data = {}
            for entry in all_entries:
                if entry.user_id not in user_data:
                    user_data[entry.user_id] = {
                        'user_id': entry.user_id,
                        'username': entry.username,
                        'points': 0,
                        'rank': 0,
                    }
                user_data[entry.user_id]['points'] += entry.points if entry.points else 0
            
            # Sort by points (descending) and assign ranks
            sorted_users = sorted(
                user_data.values(),
                key=lambda x: x['points'],
                reverse=True
            )
            
            for idx, user in enumerate(sorted_users, 1):
                user['rank'] = idx
            
            # Return top N
            top_list = sorted_users[:limit]
            
            return Response({
                'limit': limit,
                'count': len(top_list),
                'results': top_list,
            })
        except Exception as e:
            logger.error(f"Error retrieving global rankings: {str(e)}")
            return Response(
                {'results': []},
                status=status.HTTP_200_OK
            )


class GlobalPlayerStatsView(generics.GenericAPIView):
    """Get global statistics for a specific player."""
    permission_classes = [AllowAny]
    
    def get(self, request, user_id, *args, **kwargs):
        try:
            # Get player's global rank
            all_entries = LeaderboardEntry.objects.all()
            
            # Group by user_id and sum points
            user_data = {}
            for entry in all_entries:
                if entry.user_id not in user_data:
                    user_data[entry.user_id] = {
                        'user_id': entry.user_id,
                        'username': entry.username,
                        'points': 0,
                    }
                user_data[entry.user_id]['points'] += entry.points if entry.points else 0
            
            # Sort by points and assign ranks
            sorted_users = sorted(
                user_data.values(),
                key=lambda x: x['points'],
                reverse=True
            )
            
            # Find player's rank
            player_rank = None
            player_points = 0
            for idx, user in enumerate(sorted_users, 1):
                if user['user_id'] == user_id:
                    player_rank = idx
                    player_points = user['points']
                    break
            
            if player_rank is None:
                return Response(
                    {'error': 'Player not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get match statistics
            from apps.users.models import UserStatistics
            try:
                stats = UserStatistics.objects.get(user_id=user_id)
                match_stats = {
                    'total_matches': stats.total_matches,
                    'wins': stats.match_wins,
                    'losses': stats.match_losses,
                    'draws': stats.match_draws,
                    'win_rate': stats.win_rate,
                    'goals_scored': stats.goals_scored,
                }
            except:
                match_stats = {
                    'total_matches': 0,
                    'wins': 0,
                    'losses': 0,
                    'draws': 0,
                    'win_rate': 0.0,
                    'goals_scored': 0,
                }
            
            return Response({
                'user_id': user_id,
                'username': user_data[user_id]['username'] if user_id in user_data else '',
                'rank': player_rank,
                'points': player_points,
                **match_stats,
            })
        except Exception as e:
            logger.error(f"Error retrieving player stats: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve player statistics'},
                status=status.HTTP_400_BAD_REQUEST
            )

