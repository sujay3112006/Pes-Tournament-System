"""Auctions App Views"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import timedelta

from apps.auctions.models import Auction, AuctionBid
from apps.auctions.serializers import (
    AuctionListSerializer,
    AuctionDetailSerializer,
    StartAuctionSerializer,
    PlaceBidSerializer,
    AuctionBidSerializer,
    AuctionStatsSerializer,
)
import uuid
import logging

logger = logging.getLogger(__name__)


class StartAuctionView(generics.GenericAPIView):
    """Create and start a new auction."""
    serializer_class = StartAuctionSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, tournament_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Check if auction already exists for this player in tournament
            existing = Auction.objects(
                tournament_id=tournament_id,
                player_id=serializer.validated_data['player_id'],
                status__in=['pending', 'live']
            )
            if existing:
                return Response(
                    {'error': 'An active auction already exists for this player in this tournament'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create auction
            now = timezone.now()
            duration = timedelta(minutes=serializer.validated_data['duration_minutes'])
            
            auction = Auction(
                auction_id=str(uuid.uuid4()),
                tournament_id=tournament_id,
                player_id=serializer.validated_data['player_id'],
                player_username=serializer.validated_data['player_username'],
                starting_bid=serializer.validated_data['starting_bid'],
                current_bid=None,
                start_time=now,
                end_time=now + duration,
                status='pending',
                player_rating=serializer.validated_data.get('player_rating', ''),
                player_image_url=serializer.validated_data.get('player_image_url', ''),
            )
            auction.save()
            
            return Response(
                {
                    'message': 'Auction created successfully',
                    'auction_id': auction.auction_id,
                    'status': auction.status,
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Error creating auction: {str(e)}")
            return Response(
                {'error': 'Failed to create auction'},
                status=status.HTTP_400_BAD_REQUEST
            )


class TournamentAuctionsView(generics.ListAPIView):
    """Get all auctions for a tournament."""
    serializer_class = AuctionListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        tournament_id = self.kwargs.get('tournament_id')
        queryset = Auction.objects(tournament_id=tournament_id)
        
        # Filter by status
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset(status=status_param)
        
        return queryset.order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(queryset),
            'auctions': serializer.data,
        })


class ActiveAuctionsView(generics.ListAPIView):
    """Get all active (live) auctions."""
    serializer_class = AuctionListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        now = timezone.now()
        queryset = Auction.objects(
            status='live',
            end_time__gt=now
        ).order_by('end_time')
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(queryset),
            'active_auctions': serializer.data,
        })


class AuctionDetailView(generics.RetrieveAPIView):
    """Get auction details with live state."""
    serializer_class = AuctionDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'auction_id'
    lookup_url_kwarg = 'auction_id'
    
    def retrieve(self, request, *args, **kwargs):
        auction_id = kwargs.get('auction_id')
        
        try:
            auction = Auction.objects.get(auction_id=auction_id)
            serializer = self.get_serializer(auction)
            return Response(serializer.data)
        except Auction.DoesNotExist:
            return Response(
                {'error': 'Auction not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class PlaceBidView(generics.GenericAPIView):
    """Place a bid on an auction."""
    serializer_class = PlaceBidSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, auction_id, *args, **kwargs):
        try:
            auction = Auction.objects.get(auction_id=auction_id)
        except Auction.DoesNotExist:
            return Response(
                {'error': 'Auction not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bid_amount = serializer.validated_data['bid_amount']
        
        # Check auction is live
        now = timezone.now()
        if auction.status != 'live' or now > auction.end_time:
            return Response(
                {'error': 'Auction is not active'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check bid is higher than starting/current bid
        minimum_bid = auction.starting_bid if not auction.current_bid else auction.current_bid
        if bid_amount <= minimum_bid:
            min_next_bid = minimum_bid if not auction.current_bid else minimum_bid + max(10, int(minimum_bid * 0.1))
            return Response(
                {
                    'error': f'Bid must be higher than current bid',
                    'current_bid': auction.current_bid,
                    'minimum_next_bid': min_next_bid,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check user has enough coins
        try:
            from apps.users.models import User
            user = User.objects.get(user_id=request.user.user_id)
            if user.coins < bid_amount:
                return Response(
                    {
                        'error': 'Insufficient coins',
                        'user_coins': user.coins,
                        'bid_amount': bid_amount,
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Error checking user coins: {str(e)}")
            return Response(
                {'error': 'Failed to verify user coins'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Record the bid
            bid = AuctionBid(
                bid_id=str(uuid.uuid4()),
                auction_id=auction_id,
                bidder_id=request.user.user_id,
                bidder_username=request.user.username,
                bid_amount=bid_amount,
            )
            bid.save()
            
            # Update auction
            auction.current_bid = bid_amount
            auction.highest_bidder_id = request.user.user_id
            auction.highest_bidder_username = request.user.username
            auction.total_bids += 1
            auction.status = 'live'  # Ensure status is live
            auction.updated_at = now
            auction.save()
            
            return Response(
                {
                    'message': 'Bid placed successfully',
                    'auction_id': auction_id,
                    'current_bid': auction.current_bid,
                    'highest_bidder': request.user.username,
                    'total_bids': auction.total_bids,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error placing bid: {str(e)}")
            return Response(
                {'error': 'Failed to place bid'},
                status=status.HTTP_400_BAD_REQUEST
            )


class AuctionBidHistoryView(generics.ListAPIView):
    """Get bid history for an auction."""
    serializer_class = AuctionBidSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        auction_id = self.kwargs.get('auction_id')
        queryset = AuctionBid.objects(auction_id=auction_id).order_by('-bid_time')
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': len(queryset),
            'bids': serializer.data,
        })


class UserAuctionStatsView(generics.GenericAPIView):
    """Get auction statistics for a user."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id=None, *args, **kwargs):
        if user_id is None:
            user_id = request.user.user_id
        
        try:
            # Count auctions and bids
            total_auctions = len(Auction.objects(highest_bidder_id=user_id))
            active_bids = len(AuctionBid.objects(bidder_id=user_id))
            
            # Get won auctions (sold status + highest bidder)
            won_items = len(Auction.objects(
                highest_bidder_id=user_id,
                status='sold'
            ))
            
            # Calculate total spent
            bids = AuctionBid.objects(bidder_id=user_id)
            total_spent = sum(bid.bid_amount for bid in bids) if bids else 0
            
            # Active auctions count
            now = timezone.now()
            active_auctions = len(Auction.objects(
                highest_bidder_id=user_id,
                status='live',
                end_time__gt=now
            ))
            
            return Response({
                'user_id': user_id,
                'total_bids_placed': active_bids,
                'items_won': won_items,
                'total_coins_spent': total_spent,
                'active_auctions': active_auctions,
            })
        except Exception as e:
            logger.error(f"Error getting auction stats: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve statistics'},
                status=status.HTTP_400_BAD_REQUEST
            )
