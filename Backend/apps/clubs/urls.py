"""Clubs App URLs"""
from django.urls import path
from apps.clubs.views import (
    CreateClubView,
    AllClubsView,
    ClubDetailView,
    JoinClubView,
    LeaveClubView,
    UserClubsView,
    ClubStatsView,
    ClubMembersView,
    UpdateClubView,
)

urlpatterns = [
    # Club CRUD
    path('clubs/create/', CreateClubView.as_view(), name='create_club'),
    path('clubs/', AllClubsView.as_view(), name='all_clubs'),
    path('clubs/<str:club_id>/', ClubDetailView.as_view(), name='club_detail'),
    path('clubs/<str:club_id>/update/', UpdateClubView.as_view(), name='update_club'),
    
    # Membership
    path('clubs/join/', JoinClubView.as_view(), name='join_club'),
    path('clubs/leave/', LeaveClubView.as_view(), name='leave_club'),
    path('my-clubs/', UserClubsView.as_view(), name='user_clubs'),
    
    # Info
    path('clubs/<str:club_id>/stats/', ClubStatsView.as_view(), name='club_stats'),
    path('clubs/<str:club_id>/members/', ClubMembersView.as_view(), name='club_members'),
]
