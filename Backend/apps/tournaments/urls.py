"""Tournaments App URLs"""
from django.urls import path
from apps.tournaments.views import (
    CreateTournamentView,
    TournamentListView,
    TournamentDetailView,
    JoinTournamentView,
    MyTournamentsView,
    JoinedTournamentsView,
    LeaveTournamentView,
)

urlpatterns = [
    # Tournament CRUD
    path('tournaments/create/', CreateTournamentView.as_view(), name='create_tournament'),
    path('tournaments/', TournamentListView.as_view(), name='tournament_list'),
    path('tournaments/<str:tournament_id>/', TournamentDetailView.as_view(), name='tournament_detail'),
    
    # Tournament participation
    path('tournaments/<str:tournament_id>/join/', JoinTournamentView.as_view(), name='join_tournament'),
    path('tournaments/<str:tournament_id>/leave/', LeaveTournamentView.as_view(), name='leave_tournament'),
    
    # User tournaments
    path('my-tournaments/', MyTournamentsView.as_view(), name='my_tournaments'),
    path('joined-tournaments/', JoinedTournamentsView.as_view(), name='joined_tournaments'),
]
