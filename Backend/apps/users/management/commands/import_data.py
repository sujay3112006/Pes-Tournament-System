"""
Django management command to import sample data into MongoDB collections
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
from apps.users.models import User, UserStatistics
from apps.clubs.models import Club, ClubMember
from apps.tournaments.models import Tournament, TournamentPlayer
from apps.matches.models import Match, MatchEvent
from apps.missions.models import Mission, UserMission
from apps.auctions.models import Auction, AuctionBid
from apps.leaderboard.models import Leaderboard, LeaderboardEntry
from apps.reports.models import Report
from apps.ml.models import MLModel, PredictionCache
import uuid
import random


class Command(BaseCommand):
    help = 'Import sample data into all MongoDB collections'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data import...'))
        
        try:
            # Clear existing data
            self.clear_collections()
            
            # Import data in dependency order
            users = self.import_users()
            self.stdout.write(f'✓ Imported {len(users)} users')
            
            clubs = self.import_clubs(users)
            self.stdout.write(f'✓ Imported {len(clubs)} clubs')
            
            tournaments = self.import_tournaments(users)
            self.stdout.write(f'✓ Imported {len(tournaments)} tournaments')
            
            tournament_players = self.import_tournament_players(tournaments, users)
            self.stdout.write(f'✓ Imported {len(tournament_players)} tournament players')
            
            matches = self.import_matches(tournaments, users)
            self.stdout.write(f'✓ Imported {len(matches)} matches')
            
            self.import_match_events(matches)
            self.stdout.write(f'✓ Imported match events')
            
            missions = self.import_missions()
            self.stdout.write(f'✓ Imported {len(missions)} missions')
            
            self.import_user_missions(users, missions)
            self.stdout.write(f'✓ Imported user missions')
            
            auctions = self.import_auctions(tournaments, users)
            self.stdout.write(f'✓ Imported {len(auctions)} auctions')
            
            self.import_auction_bids(auctions, users)
            self.stdout.write(f'✓ Imported auction bids')
            
            leaderboards = self.import_leaderboards(tournaments, users)
            self.stdout.write(f'✓ Imported {len(leaderboards)} leaderboards')
            
            self.import_reports(matches, users)
            self.stdout.write(f'✓ Imported reports')
            
            self.import_ml_models()
            self.stdout.write(f'✓ Imported ML models')
            
            self.stdout.write(self.style.SUCCESS('\n✅ Data import completed successfully!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error during import: {str(e)}'))
            raise

    def clear_collections(self):
        """Clear all collections"""
        User.objects.delete()
        Club.objects.delete()
        ClubMember.objects.delete()
        Tournament.objects.delete()
        TournamentPlayer.objects.delete()
        Match.objects.delete()
        MatchEvent.objects.delete()
        Mission.objects.delete()
        UserMission.objects.delete()
        Auction.objects.delete()
        AuctionBid.objects.delete()
        Leaderboard.objects.delete()
        LeaderboardEntry.objects.delete()
        Report.objects.delete()
        MLModel.objects.delete()
        PredictionCache.objects.delete()

    def import_users(self):
        """Import sample users"""
        users = []
        user_data = [
            {'username': 'cristiano_ronaldo', 'email': 'cr7@football.com', 'first_name': 'Cristiano', 'last_name': 'Ronaldo'},
            {'username': 'lionel_messi', 'email': 'messi@football.com', 'first_name': 'Lionel', 'last_name': 'Messi'},
            {'username': 'neymar_jr', 'email': 'neymar@football.com', 'first_name': 'Neymar', 'last_name': 'Jr'},
            {'username': 'kylian_mbappe', 'email': 'mbappe@football.com', 'first_name': 'Kylian', 'last_name': 'Mbappé'},
            {'username': 'robert_lewandowski', 'email': 'lewy@football.com', 'first_name': 'Robert', 'last_name': 'Lewandowski'},
            {'username': 'joao_felix', 'email': 'joao@football.com', 'first_name': 'João', 'last_name': 'Felix'},
            {'username': 'vinicius_junior', 'email': 'vini@football.com', 'first_name': 'Vinicius', 'last_name': 'Junior'},
            {'username': 'erling_haaland', 'email': 'haaland@football.com', 'first_name': 'Erling', 'last_name': 'Haaland'},
            {'username': 'sadio_mane', 'email': 'mane@football.com', 'first_name': 'Sadio', 'last_name': 'Mané'},
            {'username': 'mohamed_salah', 'email': 'salah@football.com', 'first_name': 'Mohamed', 'last_name': 'Salah'},
        ]
        
        for data in user_data:
            user = User(
                username=data['username'],
                email=data['email'],
                password_hash=make_password('Password123'),
                first_name=data['first_name'],
                last_name=data['last_name'],
                coins=random.randint(500, 5000),
                bio=f"Professional footballer - {data['first_name']}",
                is_verified=True,
                is_premium=random.choice([True, False]),
                is_active=True,
                stats={
                    'wins': random.randint(10, 100),
                    'losses': random.randint(5, 50),
                    'tournaments': random.randint(3, 20),
                    'rating': round(random.uniform(4.0, 5.0), 2)
                }
            )
            user.save()
            users.append(user)
            
            # Create user statistics
            wins = random.randint(10, 50)
            matches = wins + random.randint(5, 50)
            win_rate = (wins / matches * 100) if matches > 0 else 0
            
            UserStatistics(
                user_id=user.user_id,
                total_tournaments=random.randint(1, 10),
                total_matches=matches,
                match_wins=wins,
                match_losses=matches - wins,
                match_draws=0,
                win_rate=round(win_rate, 2),
                goals_scored=random.randint(10, 100),
                goals_conceded=random.randint(5, 50),
                points=random.randint(50, 500)
            ).save()
        
        return users

    def import_clubs(self, users):
        """Import sample clubs"""
        clubs = []
        club_names = [
            'Manchester United FC', 'Real Madrid CF', 'Barcelona FC',
            'Liverpool FC', 'Bayern Munich', 'Paris Saint-Germain',
            'Juventus FC', 'Ajax Amsterdam', 'AC Milan', 'Chelsea FC'
        ]
        
        for i, club_name in enumerate(club_names):
            owner = users[i % len(users)]
            club = Club(
                name=club_name,
                description=f'{club_name} is a professional football club.',
                owner_id=owner.user_id,
                owner_username=owner.username,
                members=[u.user_id for u in random.sample(users, k=random.randint(3, 8))],
                member_count=random.randint(3, 8),
                founded_date=timezone.now() - timedelta(days=random.randint(100, 1000)),
                is_verified=True,
                total_tournaments=random.randint(5, 30),
                total_wins=random.randint(10, 50),
                stats={
                    'wins': random.randint(20, 100),
                    'losses': random.randint(5, 40),
                    'points': random.randint(100, 500)
                }
            )
            club.save()
            clubs.append(club)
            
            # Add club members
            for member_user in club.members:
                role = 'owner' if member_user == owner.user_id else random.choice(['admin', 'member'])
                member = ClubMember(
                    club_id=club.club_id,
                    user_id=member_user,
                    username=next(u.username for u in users if u.user_id == member_user),
                    role=role,
                    contribution_score=random.randint(10, 500)
                )
                member.save()
        
        return clubs

    def import_tournaments(self, users):
        """Import sample tournaments"""
        tournaments = []
        tournament_names = [
            'Spring Championship 2025',
            'Summer Cup',
            'Elite Players League',
            'International Tournament',
            'Pro Division Finals'
        ]
        
        for name in tournament_names:
            creator = random.choice(users)
            tournament = Tournament(
                name=name,
                description=f'An exciting {name} for competitive players.',
                creator_id=creator.user_id,
                start_date=timezone.now() + timedelta(days=random.randint(1, 30)),
                end_date=timezone.now() + timedelta(days=random.randint(31, 60)),
                format=random.choice(['Knockout', 'League']),
                max_players=random.choice([8, 16, 32]),
                current_players=random.randint(4, 30),
                status=random.choice(['registration', 'active', 'completed']),
                rules='Standard football rules apply.',
                prize_pool=random.randint(1000, 10000),
                location='Online',
                is_public=True
            )
            tournament.save()
            tournaments.append(tournament)
        
        return tournaments

    def import_tournament_players(self, tournaments, users):
        """Import tournament players"""
        players = []
        for tournament in tournaments:
            selected_users = random.sample(users, k=min(len(users), tournament.current_players))
            for user in selected_users:
                player = TournamentPlayer(
                    tournament_id=tournament.tournament_id,
                    user_id=user.user_id,
                    username=user.username,
                    status=random.choice(['active', 'eliminated']),
                    points=random.randint(0, 50),
                    matches_played=random.randint(0, 10),
                    wins=random.randint(0, 8),
                    losses=random.randint(0, 8),
                    draws=random.randint(0, 3)
                )
                player.save()
                players.append(player)
        
        return players

    def import_matches(self, tournaments, users):
        """Import sample matches"""
        matches = []
        for tournament in tournaments:
            for _ in range(random.randint(3, 10)):
                player1, player2 = random.sample(users, k=2)
                status = random.choice(['scheduled', 'completed'])
                
                match = Match(
                    tournament_id=tournament.tournament_id,
                    player1_id=player1.user_id,
                    player2_id=player2.user_id,
                    player1_username=player1.username,
                    player2_username=player2.username,
                    match_date=timezone.now() + timedelta(hours=random.randint(1, 72)),
                    status=status,
                    score={'player1': random.randint(0, 5) if status == 'completed' else 0,
                           'player2': random.randint(0, 5) if status == 'completed' else 0},
                    location='Online',
                    duration=90 if status == 'completed' else None
                )
                
                if status == 'completed':
                    match.winner_id = player1.user_id if match.score['player1'] > match.score['player2'] else player2.user_id
                    match.loser_id = player2.user_id if match.winner_id == player1.user_id else player1.user_id
                
                match.save()
                matches.append(match)
        
        return matches

    def import_match_events(self, matches):
        """Import match events"""
        event_types = ['goal', 'yellow_card', 'red_card', 'substitution']
        
        for match in matches:
            if match.status == 'completed':
                for _ in range(random.randint(2, 8)):
                    event = MatchEvent(
                        match_id=match.match_id,
                        event_type=random.choice(event_types),
                        player_id=random.choice([match.player1_id, match.player2_id]),
                        minute=random.randint(1, 90),
                        description='Event in match'
                    )
                    event.save()

    def import_missions(self):
        """Import sample missions"""
        missions = []
        mission_data = [
            {'title': 'First Win', 'description': 'Win your first match', 'mission_type': 'daily', 'condition': {'type': 'wins', 'value': 1}, 'reward': {'coins': 100, 'points': 50}},
            {'title': 'Weekly Champion', 'description': 'Win 5 matches in a week', 'mission_type': 'weekly', 'condition': {'type': 'wins', 'value': 5}, 'reward': {'coins': 500, 'points': 200}},
            {'title': 'Tournament Master', 'description': 'Participate in 3 tournaments', 'mission_type': 'seasonal', 'condition': {'type': 'tournaments', 'value': 3}, 'reward': {'coins': 1000, 'points': 500}},
            {'title': 'Unbeaten', 'description': 'Win 10 consecutive matches', 'mission_type': 'special', 'condition': {'type': 'wins_streak', 'value': 10}, 'reward': {'coins': 2000, 'badge': 'unbeaten'}},
            {'title': 'Active Player', 'description': 'Play 20 matches', 'mission_type': 'daily', 'condition': {'type': 'matches_played', 'value': 20}, 'reward': {'coins': 300, 'points': 100}},
        ]
        
        for data in mission_data:
            mission = Mission(
                title=data['title'],
                description=data['description'],
                mission_type=data['mission_type'],
                condition=data['condition'],
                reward=data['reward'],
                difficulty=random.choice(['easy', 'medium', 'hard']),
                status='active',
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(days=30)
            )
            mission.save()
            missions.append(mission)
        
        return missions

    def import_user_missions(self, users, missions):
        """Import user missions"""
        for user in users:
            selected_missions = random.sample(missions, k=random.randint(2, 5))
            for mission in selected_missions:
                user_mission = UserMission(
                    user_id=user.user_id,
                    mission_id=mission.mission_id,
                    mission_title=mission.title,
                    progress=random.randint(0, mission.condition['value']),
                    condition_value=mission.condition['value'],
                    completed=random.choice([True, False])
                )
                user_mission.save()

    def import_auctions(self, tournaments, users):
        """Import sample auctions"""
        auctions = []
        for tournament in tournaments[:3]:
            for _ in range(random.randint(2, 5)):
                player = random.choice(users)
                auction = Auction(
                    tournament_id=tournament.tournament_id,
                    player_id=player.user_id,
                    player_username=player.username,
                    starting_bid=random.randint(100, 500),
                    current_bid=random.randint(200, 1000),
                    start_time=timezone.now(),
                    end_time=timezone.now() + timedelta(hours=random.randint(12, 48)),
                    status=random.choice(['live', 'sold', 'unsold']),
                    player_rating='5-star',
                    total_bids=random.randint(0, 20)
                )
                auction.save()
                auctions.append(auction)
        
        return auctions

    def import_auction_bids(self, auctions, users):
        """Import auction bids"""
        for auction in auctions:
            for _ in range(auction.total_bids):
                bidder = random.choice(users)
                bid = AuctionBid(
                    auction_id=auction.auction_id,
                    bidder_id=bidder.user_id,
                    bidder_username=bidder.username,
                    bid_amount=random.randint(auction.starting_bid, 1000)
                )
                bid.save()

    def import_leaderboards(self, tournaments, users):
        """Import leaderboards"""
        leaderboards = []
        for tournament in tournaments:
            leaderboard = Leaderboard(
                tournament_id=tournament.tournament_id,
                total_entries=tournament.current_players
            )
            leaderboard.save()
            leaderboards.append(leaderboard)
            
            # Add leaderboard entries
            selected_users = random.sample(users, k=min(len(users), tournament.current_players))
            for rank, user in enumerate(selected_users, 1):
                entry = LeaderboardEntry(
                    tournament_id=tournament.tournament_id,
                    user_id=user.user_id,
                    username=user.username,
                    rank=rank,
                    points=random.randint(10, 100),
                    matches_played=random.randint(1, 15),
                    wins=random.randint(0, 10),
                    losses=random.randint(0, 10),
                    draws=random.randint(0, 3),
                    goal_difference=random.randint(-10, 10)
                )
                entry.save()
        
        return leaderboards

    def import_reports(self, matches, users):
        """Import reports"""
        if matches:
            for match in matches[:5]:
                reporter = random.choice(users)
                report = Report(
                    match_id=match.match_id,
                    reported_by_id=reporter.user_id,
                    reported_by_username=reporter.username,
                    reported_player_id=random.choice([match.player1_id, match.player2_id]),
                    reason='Suspected cheating or rule violation',
                    description='Match outcome appears suspicious.',
                    status=random.choice(['pending', 'under_review', 'resolved']),
                    severity=random.choice(['low', 'medium', 'high']),
                    action_taken=random.choice(['match_voided', 'player_banned', 'none'])
                )
                report.save()

    def import_ml_models(self):
        """Import ML models"""
        model = MLModel(
            model_name='win_probability_model',
            model_type='random_forest',
            version=1,
            is_active=True,
            accuracy={'train_accuracy': 0.92, 'test_accuracy': 0.87},
            metrics={'precision': 0.89, 'recall': 0.85, 'f1': 0.87, 'auc': 0.91},
            training_samples=1000,
            trained_at=timezone.now(),
            features_used=['player_rating', 'recent_form', 'head_to_head', 'tournament_history'],
            status='completed'
        )
        model.save()
        
        # Add prediction cache
        cache = PredictionCache(
            player1_id=str(uuid.uuid4()),
            player2_id=str(uuid.uuid4()),
            player1_win_probability=0.65,
            player2_win_probability=0.35,
            predicted_at=timezone.now(),
            expires_at=timezone.now() + timedelta(hours=24),
            is_valid=True
        )
        cache.save()
