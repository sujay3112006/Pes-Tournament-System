"""Clubs App URLs"""
from django.urls import path
from apps.clubs.views import (
    CreateClubView,
    AllClubsView,
    ClubDetailView,
    JoinClubView,
    LeaveClubView,
    UserClubsView,
    UserClubsDetailView,
    ClubStatsView,
    ClubMembersView,
    UpdateClubView,
)

urlpatterns = [
    # Specific paths FIRST
    path('create/', CreateClubView.as_view(), name='create_club'),
    path('my-clubs/', UserClubsView.as_view(), name='user_clubs'),
    path('user/<str:user_id>/', UserClubsDetailView.as_view(), name='user_clubs_detail'),
    
    # Then generic paths
    path('', AllClubsView.as_view(), name='all_clubs'),
    path('<str:club_id>/update/', UpdateClubView.as_view(), name='update_club'),
    path('<str:club_id>/stats/', ClubStatsView.as_view(), name='club_stats'),
    path('<str:club_id>/members/', ClubMembersView.as_view(), name='club_members'),
    path('<str:club_id>/', ClubDetailView.as_view(), name='club_detail'),
    
    # Actions
    path('join/', JoinClubView.as_view(), name='join_club'),
    path('leave/', LeaveClubView.as_view(), name='leave_club'),
]
