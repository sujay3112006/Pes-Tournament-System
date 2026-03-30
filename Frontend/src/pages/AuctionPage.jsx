import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Card from '../components/Card'
import PlayerCard from '../components/PlayerCard'
import Badge from '../components/Badge'

export default function AuctionPage() {
  const [timeRemaining, setTimeRemaining] = useState(120)
  const [currentBid, setCurrentBid] = useState(5000)
  const [myBid, setMyBid] = useState('')
  const [selectedPlayer, setSelectedPlayer] = useState(0)

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeRemaining(t => t > 0 ? t - 1 : 0)
    }, 1000)
    return () => clearInterval(timer)
  }, [])

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const players = [
    { id: 1, name: 'Cristiano', position: 'ST', rating: 95, image: '/placeholder.jpg' },
    { id: 2, name: 'Lewandowski', position: 'ST', rating: 93, image: '/placeholder.jpg' },
    { id: 3, name: 'De Bruyne', position: 'CM', rating: 91, image: '/placeholder.jpg' },
  ]

  const handleBid = () => {
    if (parseInt(myBid) > currentBid) {
      setCurrentBid(parseInt(myBid))
      setMyBid('')
    }
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">💰 Live Auction</h1>
        <p className="text-gray-400">Bid on exclusive eFootball players</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        {/* Main Auction */}
        <div className="lg:col-span-2">
          <Card variant="glow">
            <div className="p-8">
              {/* Current Player */}
              <div className="mb-8">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-2xl font-bold text-white">Now Auctioning</h2>
                  <Badge variant="success">🔴 LIVE</Badge>
                </div>
                
                {/* Large Player Card */}
                <motion.div
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  key={players[selectedPlayer].id}
                  className="relative aspect-video rounded-xl overflow-hidden mb-6 glassmorphism border border-neon-blue/50 shadow-glow-lg"
                >
                  <div className="absolute inset-0 bg-gradient-to-b from-dark-800 to-dark-900 flex items-center justify-center">
                    <div className="text-center">
                      <div className="text-8xl mb-4">⚽</div>
                      <h3 className="text-3xl font-bold text-neon-blue mb-2">{players[selectedPlayer].name}</h3>
                      <p className="text-gray-400">{players[selectedPlayer].position} • Rating {players[selectedPlayer].rating}</p>
                    </div>
                  </div>
                  <div className="absolute top-4 right-4 bg-neon-purple text-white px-4 py-2 rounded-full font-bold">
                    {players[selectedPlayer].rating}
                  </div>
                </motion.div>
              </div>

              {/* Bidding Section */}
              <div className="bg-dark-800/50 rounded-lg p-6 mb-6">
                <div className="grid grid-cols-2 gap-4 mb-6">
                  {/* Current Bid */}
                  <div>
                    <p className="text-gray-400 text-sm mb-1">Current Bid</p>
                    <p className="text-3xl font-bold text-neon-blue">
                      ${currentBid.toLocaleString()}
                    </p>
                  </div>

                  {/* Time Remaining */}
                  <div>
                    <p className="text-gray-400 text-sm mb-1">Time Remaining</p>
                    <motion.p
                      key={timeRemaining}
                      initial={{ scale: 1.1 }}
                      animate={{ scale: 1 }}
                      className={`text-3xl font-bold ${timeRemaining < 30 ? 'text-red-400 glow-text' : 'text-neon-purple'}`}
                    >
                      {formatTime(timeRemaining)}
                    </motion.p>
                  </div>
                </div>

                {/* Bid Input */}
                <div className="flex gap-3">
                  <input
                    type="number"
                    min={currentBid + 100}
                    placeholder={`Bid at least $${(currentBid + 100).toLocaleString()}`}
                    value={myBid}
                    onChange={(e) => setMyBid(e.target.value)}
                    className="flex-1 px-4 py-3 bg-dark-900 border border-dark-600 focus:border-neon-blue rounded-lg text-white focus:outline-none"
                  />
                  <Button
                    variant="primary"
                    size="lg"
                    onClick={handleBid}
                    disabled={!myBid || parseInt(myBid) <= currentBid}
                  >
                    Place Bid
                  </Button>
                </div>
              </div>

              {/* Quick Bid Buttons */}
              <div className="grid grid-cols-4 gap-2">
                {[500, 1000, 2000, 5000].map((amount) => (
                  <Button
                    key={amount}
                    variant="secondary"
                    size="sm"
                    className="text-xs"
                    onClick={() => {
                      setMyBid(String(currentBid + amount))
                    }}
                  >
                    +${amount}
                  </Button>
                ))}
              </div>
            </div>
          </Card>
        </div>

        {/* Upcoming Players */}
        <div>
          <h3 className="text-xl font-bold text-white mb-4">📋 Up Next</h3>
          <div className="space-y-4">
            {players.map((player, idx) => (
              <motion.div
                key={player.id}
                whileHover={{ scale: 1.05 }}
                onClick={() => setSelectedPlayer(idx)}
                className={`p-4 rounded-lg cursor-pointer transition-smooth ${
                  selectedPlayer === idx
                    ? 'glassmorphism border border-neon-blue/50 shadow-glow'
                    : 'bg-dark-800 border border-dark-700 hover:border-neon-blue/30'
                }`}
              >
                <p className="font-semibold text-white">{player.name}</p>
                <p className="text-sm text-gray-400">{player.position} • {player.rating} Rating</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Bids */}
      <Card variant="glow">
        <div className="p-6">
          <h3 className="text-xl font-bold text-white mb-4">📈 Bid History</h3>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {[
              { player: 'ProGamer', amount: 6500, time: '2 min ago' },
              { player: 'NovaStorm', amount: 6000, time: '4 min ago' },
              { player: 'ProGamer', amount: 5500, time: '6 min ago' },
              { player: 'SkyKing', amount: 5000, time: '8 min ago' },
            ].map((bid, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex justify-between items-center p-3 bg-dark-800/50 rounded-lg"
              >
                <div>
                  <p className="font-semibold text-white">{bid.player}</p>
                  <p className="text-xs text-gray-400">{bid.time}</p>
                </div>
                <span className="font-bold text-neon-blue">${bid.amount.toLocaleString()}</span>
              </motion.div>
            ))}
          </div>
        </div>
      </Card>
    </motion.div>
  )
}
