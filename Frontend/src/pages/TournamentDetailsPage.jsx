import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Card from '../components/Card'
import Badge from '../components/Badge'
import ProgressBar from '../components/ProgressBar'
import Loader from '../components/Loader'
import { tournamentService, matchService } from '../services/api'

export default function TournamentDetailsPage({ user }) {
  const { id } = useParams()
  const navigate = useNavigate()
  const [tournament, setTournament] = useState(null)
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(true)
  const [joining, setJoining] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const load = async () => {
      try {
        const [tRes, mRes] = await Promise.all([
          tournamentService.getById(id),
          matchService.getTournamentMatches(id),
        ])
        setTournament(tRes.data)
        const matches = mRes.data.matches || mRes.data.results || (Array.isArray(mRes.data) ? mRes.data : [])
        setMatches(matches)
      } catch (err) {
        console.error('Failed to load tournament:', err)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [id])

  const handleJoin = async () => {
    setJoining(true)
    setError('')
    try {
      await tournamentService.join(id)
      const { data } = await tournamentService.getById(id)
      setTournament(data)
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to join tournament')
    } finally {
      setJoining(false)
    }
  }

  if (loading) return <div className="flex justify-center py-20"><Loader message="Loading tournament..." /></div>
  if (!tournament) return <p className="text-gray-400 text-center py-20">Tournament not found.</p>

  const isRegistered = tournament.players?.some?.(p => p.user_id === user?.user_id)
  const spotsLeft = tournament.max_players - tournament.current_players

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <div className="mb-8">
        <Button variant="ghost" size="sm" onClick={() => navigate(-1)} className="mb-4">← Back</Button>
        <h1 className="text-4xl font-bold text-white mb-2">{tournament.name}</h1>
        <p className="text-gray-400">{tournament.description}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <Card variant="glow">
            <div className="p-6">
              <h2 className="text-2xl font-bold text-white mb-4">Tournament Details</h2>
              <div className="grid grid-cols-2 gap-4">
                {[
                  { label: 'Format', value: tournament.format, color: 'text-neon-blue' },
                  { label: 'Status', value: tournament.status, badge: true },
                  { label: 'Prize Pool', value: `💰 ${tournament.prize_pool?.toLocaleString() ?? 0} coins`, color: 'text-neon-pink' },
                  { label: 'Start Date', value: tournament.start_date ? new Date(tournament.start_date).toLocaleDateString() : '—', color: 'text-white' },
                  { label: 'Max Players', value: tournament.max_players, color: 'text-white' },
                  { label: 'Location', value: tournament.location || 'Virtual', color: 'text-white' },
                ].map(({ label, value, color, badge }) => (
                  <div key={label}>
                    <p className="text-gray-400 text-sm mb-1">{label}</p>
                    {badge
                      ? <Badge variant={tournament.status === 'active' ? 'success' : 'primary'}>{value}</Badge>
                      : <p className={`text-lg font-semibold ${color}`}>{value}</p>
                    }
                  </div>
                ))}
              </div>
            </div>
          </Card>

          {/* Matches */}
          {matches.length > 0 && (
            <Card variant="glow">
              <div className="p-6">
                <h2 className="text-2xl font-bold text-white mb-4">Matches</h2>
                <div className="space-y-2">
                  {matches.map((m) => (
                    <div
                      key={m.match_id}
                      className="flex items-center justify-between p-3 bg-dark-800 rounded-lg hover:bg-dark-700 cursor-pointer transition-smooth"
                      onClick={() => navigate(`/match/${m.match_id}`)}
                    >
                      <span className="text-white font-semibold">{m.player1_username} vs {m.player2_username}</span>
                      <div className="flex items-center gap-3">
                        {m.score && <span className="text-neon-blue font-bold">{m.score.player1} - {m.score.player2}</span>}
                        <Badge variant={m.status === 'completed' ? 'success' : m.status === 'live' ? 'danger' : 'primary'} size="sm">
                          {m.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </Card>
          )}

          {/* Players */}
          <Card variant="glow">
            <div className="p-6">
              <h2 className="text-2xl font-bold text-white mb-4">
                Registered Players ({tournament.current_players}/{tournament.max_players})
              </h2>
              <ProgressBar value={tournament.current_players} max={tournament.max_players} label="Registration Progress" />
            </div>
          </Card>
        </div>

        {/* Sidebar */}
        <div>
          <Card variant="glow">
            <div className="p-6 space-y-4">
              {error && <p className="text-red-400 text-sm">{error}</p>}
              <div>
                <p className="text-gray-400 text-sm mb-2">Your Status</p>
                <Badge variant={isRegistered ? 'success' : 'warning'}>
                  {isRegistered ? '✓ Registered' : 'Not Registered'}
                </Badge>
              </div>

              {!isRegistered && tournament.status === 'registration' && (
                <Button variant="primary" size="lg" className="w-full" onClick={handleJoin} isLoading={joining}>
                  Join Tournament
                </Button>
              )}
              {isRegistered && (
                <Button variant="primary" size="lg" className="w-full" onClick={() => navigate(`/leaderboard`)}>
                  View Leaderboard
                </Button>
              )}

              <div className="pt-4 border-t border-dark-700 space-y-3">
                <h3 className="font-semibold text-white">Quick Stats</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Spots Left</span>
                    <span className="font-semibold text-neon-blue">{spotsLeft}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Format</span>
                    <span className="font-semibold text-white">{tournament.format}</span>
                  </div>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </motion.div>
  )
}
