"""Auctions App Views"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.auctions.models import Auction, AuctionBid
from apps.auctions.serializers import AuctionSerializer, AuctionBidSerializer


class AuctionViewSet(viewsets.ModelViewSet):
    """Auction ViewSet."""
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Auction.objects()
    
    @action(detail=True, methods=['post'])
    def place_bid(self, request, pk=None):
        """Place a bid on an auction."""
        auction_id = pk
        bid_amount = request.data.get('bid_amount')
        
        try:
            auction = Auction.objects.get(auction_id=auction_id)
            
            if bid_amount <= auction.current_bid:
                return Response(
                    {'error': 'Bid must be higher than current bid'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            AuctionBid.objects.create(
                bid_id=f"bid_{auction_id}_{request.user.id}",
                auction_id=auction_id,
                bidder_id=str(request.user.id),
                bidder_name=request.user.username,
                bid_amount=bid_amount
            )
            
            auction.current_bid = bid_amount
            auction.highest_bidder_id = str(request.user.id)
            auction.highest_bidder_name = request.user.username
            auction.save()
            
            return Response({'message': 'Bid placed successfully'})
        except Auction.DoesNotExist:
            return Response({'error': 'Auction not found'}, status=status.HTTP_404_NOT_FOUND)


class AuctionBidViewSet(viewsets.ModelViewSet):
    """Auction Bid ViewSet."""
    serializer_class = AuctionBidSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return AuctionBid.objects()
