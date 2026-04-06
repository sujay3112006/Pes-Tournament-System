"""
Management command to create a test user with proper password hashing
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from apps.users.models import User, UserStatistics


class Command(BaseCommand):
    help = 'Create a test user with proper password hashing'

    def handle(self, *args, **options):
        # First, let's use one of the imported users
        # We'll reset the password for cristiano_ronaldo to 'Password123'
        user = User.objects(username='cristiano_ronaldo').first()
        
        if user:
            user.password_hash = make_password('Password123')
            user.save()
            
            # Create or update UserStatistics
            try:
                stats = UserStatistics.objects.get(user_id=user.user_id)
                self.stdout.write('✓ UserStatistics already exists')
            except UserStatistics.DoesNotExist:
                UserStatistics(
                    user_id=user.user_id,
                    total_tournaments=5,
                    total_matches=25,
                    match_wins=18,
                    match_losses=7,
                    match_draws=0,
                    win_rate=72.0,
                    goals_scored=45,
                    goals_conceded=18,
                    points=200
                ).save()
                self.stdout.write('✓ UserStatistics created')
            
            self.stdout.write(self.style.SUCCESS(
                '✅ User "cristiano_ronaldo" created/updated successfully'
            ))
            self.stdout.write(self.style.HTTP_INFO(
                '\n📝 Login with these credentials:'
            ))
            self.stdout.write(self.style.HTTP_INFO(
                '  Username: cristiano_ronaldo'
            ))
            self.stdout.write(self.style.HTTP_INFO(
                '  Password: Password123'
            ))
        else:
            # Create a new test user
            user = User(
                username='testuser',
                email='test@football.com',
                password_hash=make_password('TestUser123'),
                first_name='Test',
                last_name='User',
                is_active=True,
                is_verified=True
            )
            user.save()
            
            # Create UserStatistics
            UserStatistics(
                user_id=user.user_id,
                total_tournaments=3,
                total_matches=15,
                match_wins=10,
                match_losses=5,
                match_draws=0,
                win_rate=66.67,
                goals_scored=30,
                goals_conceded=15,
                points=150
            ).save()
            
            self.stdout.write(self.style.SUCCESS(
                '✅ Test user created successfully'
            ))
            self.stdout.write(self.style.HTTP_INFO(
                '\n📝 Login with these credentials:'
            ))
            self.stdout.write(self.style.HTTP_INFO(
                '  Username: testuser'
            ))
            self.stdout.write(self.style.HTTP_INFO(
                '  Password: TestUser123'
            ))
