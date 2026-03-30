import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Card from '../components/Card'
import { getTimeRemaining } from '../utils/helpers'

export default function LiveMatchTrackerPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [matchTime, setMatchTime] = useState(0)
  const [score, setScore] = useState({ player1: 0, player2: 0 })
  const [events, setEvents] = useState([
    { time: '45:30', type: 'goal', player: 'ProGamer', icon: '⚽' },
    { time: '23:15', type: 'card', player: 'NovaStorm', icon: '🟥' },
    { time: '10:00', type: 'goal', player: 'NovaStorm', icon: '⚽' },
  ])

  useEffect(() => {
    const timer = setInterval(() => {
      setMatchTime(mt => mt + 1)
    }, 1000)
    return () => clearInterval(timer)
  }, [])

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <div className="mb-8">
        <Button variant="ghost" size="sm" onClick={() => navigate(-1)} className="mb-4">
          ← Back
        </Button>
        <h1 className="text-4xl font-bold text-white mb-2">⚔️ Live Match Tracker</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Scoreboard */}
        <div className="lg:col-span-2 space-y-6">
          {/* Live Scoreboard */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <Card variant="glow">
              <div className="p-8 bg-gradient-to-br from-dark-800/50 to-dark-900/50">
                {/* Match Timer */}
                <div className="text-center mb-8">
                  <p className="text-gray-400 text-sm mb-2">Elapsed Time</p>
                  <p className="text-6xl font-bold text-neon-blue glow-text">
                    {formatTime(matchTime)}
                  </p>
                  <p className="text-gray-400 text-sm mt-2">1st Half</p>
                </div>

                {/* Score Display */}
                <div className="grid grid-cols-3 gap-4 mb-8">
                  {/* Player 1 */}
                  <div className="text-center">
                    <h3 className="text-lg font-bold text-white mb-4">ProGamer</h3>
                    <motion.div
                      key={score.player1}
                      initial={{ scale: 1.2 }}
                      animate={{ scale: 1 }}
                      className="text-7xl font-bold text-neon-blue glow-text"
                    >
                      {score.player1}
                    </motion.div>
                  </div>

                  {/* VS */}
                  <div className="flex items-center justify-center">
                    <span className="text-3xl font-bold text-gray-500">-</span>
                  </div>

                  {/* Player 2 */}
                  <div className="text-center">
                    <h3 className="text-lg font-bold text-white mb-4">NovaStorm</h3>
                    <motion.div
                      key={score.player2}
                      initial={{ scale: 1.2 }}
                      animate={{ scale: 1 }}
                      className="text-7xl font-bold text-neon-purple glow-text"
                    >
                      {score.player2}
                    </motion.div>
                  </div>
                </div>

                {/* Quick Actions */}
                <div className="grid grid-cols-2 gap-4">
                  <Button
                    variant="primary"
                    size="md"
                    className="w-full"
                    onClick={() => setScore({ ...score, player1: score.player1 + 1 })}
                  >
                    ⚽ Goal P1
                  </Button>
                  <Button
                    variant="accent"
                    size="md"
                    className="w-full"
                    onClick={() => setScore({ ...score, player2: score.player2 + 1 })}
                  >
                    ⚽ Goal P2
                  </Button>
                </div>
              </div>
            </Card>
          </motion.div>

          {/* Match Events Timeline */}
          <Card variant="glow">
            <div className="p-6">
              <h2 className="text-2xl font-bold text-white mb-6">📊 Match Events</h2>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {events.map((event, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.1 }}
                    className="flex items-center gap-4 p-4 bg-dark-800/50 rounded-lg hover:bg-dark-700 transition-smooth"
                  >
                    <div className="w-12 h-12 rounded-full bg-gradient-to-r from-neon-blue to-neon-purple flex items-center justify-center text-xl">
                      {event.icon}
                    </div>
                    <div className="flex-1">
                      <p className="font-semibold text-white">{event.player}</p>
                      <p className="text-sm text-gray-400 capitalize">{event.type}</p>
                    </div>
                    <span className="text-neon-blue font-bold">{event.time}</span>
                  </motion.div>
                ))}
              </div>
            </div>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Match Info */}
          <Card variant="glow">
            <div className="p-6 space-y-4">
              <h3 className="font-bold text-white text-lg">Match Info</h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">Status</span>
                  <span className="font-semibold text-green-400">🔴 LIVE</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Prize Pool</span>
                  <span className="font-semibold text-neon-pink">💰 $500</span>
                </div>
              </div>
            </div>
          </Card>

          {/* Stats */}
          <Card variant="glow">
            <div className="p-6 space-y-4">
              <h3 className="font-bold text-white text-lg">Stats</h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="p-3 bg-dark-800 rounded-lg text-center">
                  <p className="text-gray-400 text-xs mb-1">P1 Possession</p>
                  <p className="text-lg font-bold text-neon-blue">53%</p>
                </div>
                <div className="p-3 bg-dark-800 rounded-lg text-center">
                  <p className="text-gray-400 text-xs mb-1">P2 Possession</p>
                  <p className="text-lg font-bold text-neon-purple">47%</p>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </motion.div>
  )
}
