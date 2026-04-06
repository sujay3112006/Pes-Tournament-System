import { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Card from '../components/Card'
import Badge from '../components/Badge'
import Loader from '../components/Loader'
import { auctionService, createAuctionSocket } from '../services/api'

export default function AuctionPage({ user }) {
  const [auctions, setAuctions] = useState([])
  const [selected, setSelected] = useState(null)
  const [bidHistory, setBidHistory] = useState([])
  const [myBid, setMyBid] = useState('')
  const [loading, setLoading] = useState(true)
  const [bidding, setBidding] = useState(false)
  const [error, setError] = useState('')
  const [timeRemaining, setTimeRemaining] = useState(0)
  const socketRef = useRef(null)
  const timerRef = useRef(null)

  useEffect(() => {
    auctionService.getActive()
      .then(({ data }) => {
        const list = data.results || data || []
        setAuctions(list)
        if (list.length > 0) selectAuction(list[0])
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const selectAuction = async (auction) => {
    setSelected(auction)
    setError('')
    setMyBid('')

    // Load bid history
    try {
      const { data } = await auctionService.getBidHistory(auction.auction_id)
      setBidHistory(data.results || [])
    } catch { setBidHistory([]) }

    // Countdown timer
    clearInterval(timerRef.current)
    const updateTimer = () => {
      const end = new Date(auction.end_time)
      const diff = Math.max(0, Math.floor((end - Date.now()) / 1000))
      setTimeRemaining(diff)
    }
    updateTimer()
    timerRef.current = setInterval(updateTimer, 1000)

    // WebSocket
    if (socketRef.current) socketRef.current.close()
    const ws = createAuctionSocket(auction.auction_id)
    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data)
      if (msg.type === 'bid_placed') {
        setSelected(prev => prev ? { ...prev, current_bid: msg.current_highest, total_bids: msg.total_bids } : prev)
        setBidHistory(prev => [{ bidder: msg.bidder_id, amount: msg.bid_amount, time: msg.timestamp }, ...prev])
      }
      if (msg.type === 'auction_completed') {
        setSelected(prev => prev ? { ...prev, status: 'sold' } : prev)
      }
    }
    socketRef.current = ws
  }

  useEffect(() => () => {
    clearInterval(timerRef.current)
    socketRef.current?.close()
  }, [])

  const formatTime = (s) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`

  const minNextBid = selected ? Math.ceil(Math.max(selected.current_bid * 1.1, selected.current_bid + 10)) : 0

  const handleBid = async () => {
    const amount = parseInt(myBid)
    if (!amount || amount < minNextBid) { setError(`Minimum bid is ${minNextBid} coins`); return }
    setError('')
    setBidding(true)
    try {
      await auctionService.placeBid(selected.auction_id, amount)
      setSelected(prev => prev ? { ...prev, current_bid: amount } : prev)
      setMyBid('')
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to place bid')
    } finally {
      setBidding(false)
    }
  }

  if (loading) return <div className="flex justify-center py-20"><Loader message="Loading auctions..." /></div>

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">💰 Live Auction</h1>
        <p className="text-gray-400">Bid on players using your coins</p>
      </div>

      {auctions.length === 0 && (
        <p className="text-gray-400 text-center py-20">No active auctions right now.</p>
      )}

      {auctions.length > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {/* Main Auction */}
          <div className="lg:col-span-2">
            {selected && (
              <Card variant="glow">
                <div className="p-8">
                  <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-bold text-white">Now Auctioning</h2>
                    <Badge variant={selected.status === 'live' ? 'success' : 'primary'}>
                      {selected.status === 'live' ? '🔴 LIVE' : selected.status.toUpperCase()}
                    </Badge>
                  </div>

                  <motion.div
                    key={selected.auction_id}
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="relative aspect-video rounded-xl overflow-hidden mb-6 glassmorphism border border-neon-blue/50 shadow-glow-lg"
                  >
                    <div className="absolute inset-0 bg-gradient-to-b from-dark-800 to-dark-900 flex items-center justify-center">
                      <div className="text-center">
                        <div className="text-8xl mb-4">⚽</div>
                        <h3 className="text-3xl font-bold text-neon-blue mb-2">{selected.player_username}</h3>
                        {selected.player_rating && <p className="text-gray-400">{selected.player_rating}</p>}
                      </div>
                    </div>
                  </motion.div>

                  <div className="bg-dark-800/50 rounded-lg p-6 mb-6">
                    <div className="grid grid-cols-2 gap-4 mb-6">
                      <div>
                        <p className="text-gray-400 text-sm mb-1">Current Bid</p>
                        <p className="text-3xl font-bold text-neon-blue">{selected.current_bid?.toLocaleString()} coins</p>
                      </div>
                      <div>
                        <p className="text-gray-400 text-sm mb-1">Time Remaining</p>
                        <motion.p
                          key={timeRemaining}
                          initial={{ scale: 1.1 }}
                          animate={{ scale: 1 }}
                          className={`text-3xl font-bold ${timeRemaining < 30 ? 'text-red-400' : 'text-neon-purple'}`}
                        >
                          {formatTime(timeRemaining)}
                        </motion.p>
                      </div>
                    </div>

                    {error && <p className="text-red-400 text-sm mb-3">{error}</p>}

                    {selected.status === 'live' && (
                      <>
                        <div className="flex gap-3 mb-4">
                          <input
                            type="number"
                            min={minNextBid}
                            placeholder={`Min bid: ${minNextBid} coins`}
                            value={myBid}
                            onChange={(e) => setMyBid(e.target.value)}
                            className="flex-1 px-4 py-3 bg-dark-900 border border-dark-600 focus:border-neon-blue rounded-lg text-white focus:outline-none"
                          />
                          <Button variant="primary" size="lg" onClick={handleBid} isLoading={bidding}
                            disabled={!myBid || parseInt(myBid) < minNextBid}>
                            Place Bid
                          </Button>
                        </div>
                        <div className="grid grid-cols-4 gap-2">
                          {[100, 500, 1000, 5000].map((inc) => (
                            <Button key={inc} variant="secondary" size="sm" className="text-xs"
                              onClick={() => setMyBid(String(minNextBid + inc))}>
                              +{inc}
                            </Button>
                          ))}
                        </div>
                      </>
                    )}
                  </div>
                </div>
              </Card>
            )}
          </div>

          {/* Auction List */}
          <div>
            <h3 className="text-xl font-bold text-white mb-4">📋 Active Auctions</h3>
            <div className="space-y-3">
              {auctions.map((a) => (
                <motion.div
                  key={a.auction_id}
                  whileHover={{ scale: 1.02 }}
                  onClick={() => selectAuction(a)}
                  className={`p-4 rounded-lg cursor-pointer transition-smooth ${
                    selected?.auction_id === a.auction_id
                      ? 'glassmorphism border border-neon-blue/50 shadow-glow'
                      : 'bg-dark-800 border border-dark-700 hover:border-neon-blue/30'
                  }`}
                >
                  <p className="font-semibold text-white">{a.player_username}</p>
                  <p className="text-sm text-gray-400">{a.current_bid?.toLocaleString()} coins • {a.total_bids} bids</p>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Bid History */}
      {bidHistory.length > 0 && (
        <Card variant="glow">
          <div className="p-6">
            <h3 className="text-xl font-bold text-white mb-4">📈 Bid History</h3>
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {bidHistory.map((bid, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex justify-between items-center p-3 bg-dark-800/50 rounded-lg"
                >
                  <div>
                    <p className="font-semibold text-white">{bid.bidder}</p>
                    <p className="text-xs text-gray-400">{bid.time ? new Date(bid.time).toLocaleTimeString() : ''}</p>
                  </div>
                  <span className="font-bold text-neon-blue">{bid.amount?.toLocaleString()} coins</span>
                </motion.div>
              ))}
            </div>
          </div>
        </Card>
      )}
    </motion.div>
  )
}
