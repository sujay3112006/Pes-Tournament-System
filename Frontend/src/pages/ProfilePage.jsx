import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Card from '../components/Card'
import Badge from '../components/Badge'
import Loader from '../components/Loader'
import { matchService, leaderboardService, authService } from '../services/api'

export default function ProfilePage({ user }) {
  const { id } = useParams()
  const navigate = useNavigate()
  const [profile, setProfile] = useState(null)
  const [matchHistory, setMatchHistory] = useState([])
  const [lbStats, setLbStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        // Use the id from params, or fall back to logged-in user's ID
        let playerId = id || user?.user_id
        
        // If id looks like a default/invalid value, use logged-in user
        if (!playerId || playerId === '1' || playerId === 'me') {
          playerId = user?.user_id
        }
        
        if (!playerId) {
          console.error('❌ No player ID available')
          setProfile(null)
          setLoading(false)
          return
        }

        console.log(`📊 Loading profile for player: ${playerId}`)
        
        // If loading own profile, use getProfile()
        if (playerId === user?.user_id) {
          const profileRes = await authService.getProfile()
          setProfile(profileRes.data)
        } else {
          // For other players, try to get stats
          // Note: Backend may not have a direct player profile endpoint
          setProfile(null)
        }

        // Load match stats
        try {
          const statsRes = await matchService.getPlayerStats(playerId)
          setProfile(prev => prev ? { ...prev, ...statsRes.data } : statsRes.data)
        } catch (err) {
          console.warn('⚠️ Match stats error:', err.message)
          // If this fails with a non-UUID ID, retry with logged-in user
          if (playerId !== user?.user_id && (err.response?.status === 404 || err.response?.status === 400)) {
            const statsRes = await matchService.getPlayerStats(user?.user_id)
            setProfile(prev => prev ? { ...prev, ...statsRes.data } : statsRes.data)
          }
        }

        // Load match history
        try {
          const matchRes = await matchService.getPlayerMatches(playerId, { status: 'completed', limit: 10 })
          // Backend returns { count, matches } structure
          const matches = matchRes.data.matches || matchRes.data.results || (Array.isArray(matchRes.data) ? matchRes.data : [])
          setMatchHistory(matches)
        } catch (err) {
          console.warn('⚠️ Match history error:', err.message)
          if (playerId !== user?.user_id && (err.response?.status === 404 || err.response?.status === 400)) {
            const matchRes = await matchService.getPlayerMatches(user?.user_id, { status: 'completed', limit: 10 })
            const matches = matchRes.data.matches || matchRes.data.results || (Array.isArray(matchRes.data) ? matchRes.data : [])
            setMatchHistory(matches)
          }
        }

        // Load leaderboard stats
        try {
          const lbRes = await leaderboardService.getPlayerStats(playerId)
          setLbStats(lbRes.data)
        } catch (err) {
          console.warn('⚠️ Leaderboard stats error:', err.message)
          if (playerId !== user?.user_id && (err.response?.status === 404 || err.response?.status === 400)) {
            try {
              const lbRes = await leaderboardService.getPlayerStats(user?.user_id)
              setLbStats(lbRes.data)
            } catch {}
          }
        }
      } catch (err) {
        console.error('Profile load error:', err)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [id, user])

  if (loading) return <div className="flex justify-center py-20"><Loader message="Loading profile..." /></div>
  if (!profile) return <p className="text-gray-400 text-center py-20">Player not found.</p>

  const isOwnProfile = user?.user_id === (id || user?.user_id)
  const winRate = profile.win_rate?.toFixed(1) ?? 0

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <Button variant="ghost" size="sm" onClick={() => navigate(-1)} className="mb-4">← Back</Button>

      {/* Profile Header */}
      <Card variant="glow" className="mb-8">
        <div className="p-8 bg-gradient-to-r from-neon-blue/10 to-neon-purple/10">
          <div className="flex justify-between items-start mb-6">
            <div className="flex items-center gap-6">
              <div className="w-24 h-24 rounded-full bg-gradient-to-r from-neon-blue to-neon-purple flex items-center justify-center text-4xl font-bold">
                {profile.username?.[0]?.toUpperCase() ?? '?'}
              </div>
              <div>
                <h1 className="text-4xl font-bold text-white mb-1">{profile.username}</h1>
                {lbStats && (
                  <div className="flex gap-3 mt-2">
                    <Badge variant="primary">Rank #{lbStats.rank}</Badge>
                    <Badge variant="purple">{lbStats.points} pts</Badge>
                  </div>
                )}
              </div>
            </div>
            {isOwnProfile && <Badge variant="success">You</Badge>}
          </div>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mt-6 pt-6 border-t border-white/10">
            {[
              { label: 'Matches', value: profile.total_matches ?? 0 },
              { label: 'Wins', value: profile.wins ?? 0 },
              { label: 'Losses', value: profile.losses ?? 0 },
              { label: 'Win Rate', value: `${winRate}%` },
              { label: 'Goals', value: profile.goals_scored ?? 0 },
            ].map((s, idx) => (
              <div key={idx} className="text-center">
                <p className="text-gray-400 text-sm mb-1">{s.label}</p>
                <p className="text-2xl font-bold text-neon-blue">{s.value}</p>
              </div>
            ))}
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Match History */}
        <div className="lg:col-span-2">
          <Card variant="elevated">
            <div className="p-6">
              <h2 className="text-2xl font-bold text-white mb-6">📜 Recent Matches</h2>
              {matchHistory.length === 0 && <p className="text-gray-400">No matches played yet.</p>}
              <div className="space-y-3">
                {matchHistory.map((match, idx) => {
                  const isP1 = match.player1_id === id
                  const opponent = isP1 ? match.player2_username : match.player1_username
                  const myScore = isP1 ? match.score?.player1 : match.score?.player2
                  const oppScore = isP1 ? match.score?.player2 : match.score?.player1
                  const won = match.winner_id === id
                  const isDraw = match.is_draw
                  const result = isDraw ? 'Draw' : won ? 'Win' : 'Loss'

                  return (
                    <motion.div
                      key={match.match_id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.05 }}
                      className="flex items-center justify-between p-4 bg-dark-800/50 rounded-lg hover:bg-dark-700 transition-smooth cursor-pointer"
                      onClick={() => navigate(`/match/${match.match_id}`)}
                    >
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-1">
                          <span className="font-semibold text-white">vs {opponent}</span>
                          <Badge variant={result === 'Win' ? 'success' : result === 'Loss' ? 'danger' : 'warning'} size="sm">
                            {result}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-400">{match.match_date ? new Date(match.match_date).toLocaleDateString() : ''}</p>
                      </div>
                      {match.score && (
                        <p className="text-lg font-bold text-neon-blue">{myScore} - {oppScore}</p>
                      )}
                    </motion.div>
                  )
                })}
              </div>
            </div>
          </Card>
        </div>

        {/* Sidebar Stats */}
        <div className="space-y-6">
          <Card variant="dark">
            <div className="p-6 space-y-4 text-sm">
              <h3 className="text-lg font-bold text-white">Career Stats</h3>
              {[
                { label: 'Goals Scored', value: profile.goals_scored ?? 0, color: 'text-green-400' },
                { label: 'Goals Conceded', value: profile.goals_conceded ?? 0, color: 'text-red-400' },
                { label: 'Draws', value: profile.draws ?? 0, color: 'text-yellow-400' },
              ].map((s) => (
                <div key={s.label} className="flex justify-between">
                  <span className="text-gray-400">{s.label}</span>
                  <span className={`font-semibold ${s.color}`}>{s.value}</span>
                </div>
              ))}
              {lbStats && (
                <>
                  <div className="flex justify-between pt-3 border-t border-dark-700">
                    <span className="text-gray-400">Tournaments</span>
                    <span className="font-semibold text-white">{lbStats.tournaments_participated ?? 0}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Leaderboard Pts</span>
                    <span className="font-semibold text-neon-blue">{lbStats.points ?? 0}</span>
                  </div>
                </>
              )}
            </div>
          </Card>
        </div>
      </div>
    </motion.div>
  )
}
