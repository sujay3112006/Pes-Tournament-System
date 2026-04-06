import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Card from '../components/Card'
import Badge from '../components/Badge'
import Loader from '../components/Loader'
import { matchService, createMatchSocket } from '../services/api'

export default function LiveMatchTrackerPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [match, setMatch] = useState(null)
  const [score, setScore] = useState({ player1: 0, player2: 0 })
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)
  const [connected, setConnected] = useState(false)
  const socketRef = useRef(null)

  useEffect(() => {
    matchService.getById(id)
      .then(({ data }) => {
        setMatch(data)
        if (data.score) setScore(data.score)
      })
      .catch(console.error)
      .finally(() => setLoading(false))

    // WebSocket
    const ws = createMatchSocket(id)
    ws.onopen = () => setConnected(true)
    ws.onclose = () => setConnected(false)
    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data)
      if (msg.type === 'score_updated') {
        setScore({ player1: msg.player1_score, player2: msg.player2_score })
        setEvents(prev => [{ time: new Date().toLocaleTimeString(), type: 'score', player: 'Update', icon: '⚽' }, ...prev])
      }
      if (msg.type === 'match_status_changed') {
        setMatch(prev => prev ? { ...prev, status: msg.status } : prev)
      }
      if (msg.type === 'match_completed') {
        setScore({ player1: parseInt(msg.final_score?.split('-')[0] ?? 0), player2: parseInt(msg.final_score?.split('-')[1] ?? 0) })
        setMatch(prev => prev ? { ...prev, status: 'completed', winner_id: msg.winner_id } : prev)
      }
    }
    socketRef.current = ws

    return () => ws.close()
  }, [id])

  if (loading) return <div className="flex justify-center py-20"><Loader message="Loading match..." /></div>

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <div className="mb-8">
        <Button variant="ghost" size="sm" onClick={() => navigate(-1)} className="mb-4">← Back</Button>
        <div className="flex items-center gap-4">
          <h1 className="text-4xl font-bold text-white">⚔️ Live Match Tracker</h1>
          <Badge variant={connected ? 'success' : 'warning'}>{connected ? '🔴 LIVE' : 'Connecting...'}</Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          {/* Scoreboard */}
          <Card variant="glow">
            <div className="p-8 bg-gradient-to-br from-dark-800/50 to-dark-900/50">
              <div className="grid grid-cols-3 gap-4 mb-8">
                <div className="text-center">
                  <h3 className="text-lg font-bold text-white mb-4">{match?.player1_username ?? 'Player 1'}</h3>
                  <motion.div key={score.player1} initial={{ scale: 1.2 }} animate={{ scale: 1 }}
                    className="text-7xl font-bold text-neon-blue glow-text">
                    {score.player1}
                  </motion.div>
                </div>
                <div className="flex items-center justify-center">
                  <span className="text-3xl font-bold text-gray-500">-</span>
                </div>
                <div className="text-center">
                  <h3 className="text-lg font-bold text-white mb-4">{match?.player2_username ?? 'Player 2'}</h3>
                  <motion.div key={score.player2} initial={{ scale: 1.2 }} animate={{ scale: 1 }}
                    className="text-7xl font-bold text-neon-purple glow-text">
                    {score.player2}
                  </motion.div>
                </div>
              </div>

              {match?.status === 'completed' && (
                <div className="text-center py-4 border-t border-dark-600">
                  <p className="text-2xl font-bold text-green-400">Match Completed</p>
                </div>
              )}
            </div>
          </Card>

          {/* Events Timeline */}
          <Card variant="glow">
            <div className="p-6">
              <h2 className="text-2xl font-bold text-white mb-6">📊 Match Events</h2>
              {events.length === 0 && <p className="text-gray-400">Waiting for events...</p>}
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {events.map((event, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="flex items-center gap-4 p-4 bg-dark-800/50 rounded-lg"
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
          <Card variant="glow">
            <div className="p-6 space-y-4">
              <h3 className="font-bold text-white text-lg">Match Info</h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">Status</span>
                  <span className={`font-semibold capitalize ${match?.status === 'live' ? 'text-green-400' : 'text-white'}`}>
                    {match?.status ?? '—'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">WebSocket</span>
                  <span className={`font-semibold ${connected ? 'text-green-400' : 'text-yellow-400'}`}>
                    {connected ? 'Connected' : 'Reconnecting...'}
                  </span>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </motion.div>
  )
}
