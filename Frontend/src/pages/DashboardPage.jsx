import { motion } from 'framer-motion'
import { useState, useEffect } from 'react'
import Button from '../components/Button'
import Card from '../components/Card'
import Badge from '../components/Badge'
import Loader from '../components/Loader'
import { useNavigate } from 'react-router-dom'
import { tournamentService, matchService, authService } from '../services/api'

export default function DashboardPage({ user }) {
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)
  const [tournaments, setTournaments] = useState([])
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const load = async () => {
      try {
        console.log('📊 Dashboard: Loading data...')
        console.log('📊 Dashboard: User prop:', user)
        
        const profileRes = await authService.getProfile()
        console.log('✅ Dashboard: Profile loaded:', profileRes.data)
        setStats(profileRes.data)
        
        // Load tournaments
        try {
          const tourRes = await tournamentService.getAll({ status: 'active', page: 1 })
          const tournaments = tourRes.data.tournaments || tourRes.data.results || (Array.isArray(tourRes.data) ? tourRes.data : [])
          setTournaments(tournaments)
          console.log('✅ Dashboard: Tournaments loaded:', tournaments?.length || 0)
        } catch (tourErr) {
          console.warn('⚠️ Dashboard: Failed to load tournaments:', tourErr.message)
        }

        // Load matches if user_id is available
        if (profileRes.data?.user_id) {
          try {
            const matchRes = await matchService.getPlayerMatches(profileRes.data.user_id, { status: 'scheduled', limit: 5 })
            const matches = matchRes.data.matches || matchRes.data.results || (Array.isArray(matchRes.data) ? matchRes.data : [])
            setMatches(matches)
            console.log('✅ Dashboard: Matches loaded:', matches?.length || 0)
          } catch (matchErr) {
            console.warn('⚠️ Dashboard: Failed to load matches:', matchErr.message)
          }
        }
      } catch (err) {
        console.error('❌ Dashboard: Error loading data:', err)
        console.error('❌ Error response:', err.response?.data)
        console.error('❌ Error status:', err.response?.status)
        
        // Only set error, don't redirect automatically
        if (err.response?.status === 401) {
          setError('Your session has expired. Please log in again.')
          // Redirect after a delay to show the error
          setTimeout(() => navigate('/login'), 2000)
        } else {
          setError('Failed to load dashboard. Please try refreshing.')
        }
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [navigate])

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.1, delayChildren: 0.2 } }
  }
  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } }
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-20 min-h-screen">
        <div className="text-center">
          <div className="text-6xl mb-4">⚠️</div>
          <h2 className="text-3xl font-black text-neon-pink mb-3">{error}</h2>
          <p className="text-gray-400 mb-6">Redirecting to login...</p>
          <Loader message="Redirecting..." />
        </div>
      </div>
    )
  }

  if (loading) return <div className="flex justify-center py-20"><Loader message="Loading dashboard..." /></div>

  const username = stats?.username || user?.username || 'Player'
  const coins = stats?.coins ?? 0
  const wins = stats?.stats?.wins ?? 0
  const losses = stats?.stats?.losses ?? 0
  const rating = stats?.stats?.rating ?? 0

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
      {/* Hero Header */}
      <motion.div className="mb-10" initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <motion.h1
          className="text-5xl font-black bg-gradient-to-r from-neon-blue via-neon-cyan to-neon-purple bg-clip-text text-transparent mb-3 drop-shadow-xl"
          animate={{ scale: [0.98, 1, 0.98] }}
          transition={{ duration: 3, repeat: Infinity }}
        >
          Welcome back, <span className="text-neon-cyan">{username}</span>!
        </motion.h1>
        <motion.p
          className="text-gray-300 font-semibold text-lg"
          animate={{ opacity: [0.7, 1, 0.7] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          🎮 Ready to dominate? Your tournament awaits...
        </motion.p>
      </motion.div>

      {/* Stats Grid */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-10"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {[
          { label: 'COINS', value: coins.toLocaleString(), icon: '💰', color: 'from-emerald-400 to-green-400' },
          { label: 'WINS', value: wins, icon: '🏆', color: 'from-neon-cyan to-neon-blue' },
          { label: 'LOSSES', value: losses, icon: '📉', color: 'from-neon-pink to-red-400' },
          { label: 'RATING', value: rating, icon: '⭐', color: 'from-yellow-400 to-orange-400' },
        ].map((stat, idx) => (
          <motion.div key={idx} variants={itemVariants}>
            <motion.div whileHover={{ y: -12, scale: 1.02 }} className="h-full">
              <Card variant="premium" className="h-full">
                <div className={`p-6 text-center bg-gradient-to-br ${stat.color} bg-opacity-5`}>
                  <motion.div className="text-5xl mb-3" animate={{ scale: [1, 1.1, 1] }} transition={{ duration: 2, repeat: Infinity }}>
                    {stat.icon}
                  </motion.div>
                  <p className="text-gray-400 text-xs font-black uppercase tracking-widest mb-2">{stat.label}</p>
                  <motion.p className={`text-3xl font-black bg-gradient-to-r ${stat.color} bg-clip-text text-transparent`}>
                    {stat.value}
                  </motion.p>
                </div>
              </Card>
            </motion.div>
          </motion.div>
        ))}
      </motion.div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-10">
        {/* Active Tournaments */}
        <motion.div className="lg:col-span-2" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }}>
          <h2 className="text-3xl font-black text-white mb-5 flex items-center gap-3 drop-shadow-lg">
            🏆 ACTIVE TOURNAMENTS
            <span className="animate-pulse-urgent inline-block w-3 h-3 bg-neon-cyan rounded-full"></span>
          </h2>
          <div className="space-y-4">
            {tournaments.length === 0 && (
              <p className="text-gray-400">No active tournaments right now.</p>
            )}
            {tournaments.map((t, idx) => (
              <motion.div
                key={t.tournament_id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + idx * 0.1 }}
                onClick={() => navigate(`/tournaments/${t.tournament_id}`)}
                className="cursor-pointer"
              >
                <Card variant="glow" hover>
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-5">
                      <div className="flex-1">
                        <h3 className="text-xl font-black text-white drop-shadow-lg">{t.name}</h3>
                        <Badge variant="primary" size="md" className="mt-3 font-bold">
                          {t.current_players}/{t.max_players} Players
                        </Badge>
                      </div>
                      <Badge variant={t.status === 'active' ? 'success' : 'primary'} size="md" className="font-black">
                        {t.status.toUpperCase()}
                      </Badge>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-neon-cyan font-black text-lg drop-shadow-lg">
                        💰 {t.prize_pool?.toLocaleString() ?? 0} coins
                      </span>
                      <Button variant="secondary" size="md" className="font-bold">VIEW DETAILS</Button>
                    </div>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Quick Actions */}
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }}>
          <h2 className="text-3xl font-black text-white mb-5 drop-shadow-lg">⚡ QUICK ACTIONS</h2>
          <div className="space-y-3">
            {[
              { label: 'JOIN TOURNAMENT', action: '/tournaments', icon: '🎮', color: 'primary' },
              { label: 'CREATE TOURNAMENT', action: '/tournaments/create', icon: '🏗️', color: 'accent' },
              { label: 'LIVE AUCTION', action: '/auction', icon: '💎', color: 'secondary' },
              { label: 'DAILY MISSIONS', action: '/missions', icon: '🎯', color: 'ghost' },
            ].map((action, idx) => (
              <motion.div key={idx} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 + idx * 0.08 }}>
                <Button variant={action.color} size="lg" className="w-full justify-center font-black text-base" onClick={() => navigate(action.action)}>
                  <span className="mr-2">{action.icon}</span>
                  {action.label}
                </Button>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Upcoming Matches */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6 }}>
        <h2 className="text-3xl font-black text-white mb-5 flex items-center gap-3 drop-shadow-lg">
          ⚔️ UPCOMING BATTLES
          <span className="animate-pulse-urgent inline-block w-3 h-3 bg-neon-pink rounded-full"></span>
        </h2>
        {matches.length === 0 && <p className="text-gray-400">No upcoming matches scheduled.</p>}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {matches.map((match, idx) => {
            const opponent = match.player1_id === stats?.user_id ? match.player2_username : match.player1_username
            return (
              <motion.div
                key={match.match_id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 + idx * 0.1 }}
                whileHover={{ y: -8 }}
                onClick={() => navigate(`/match/${match.match_id}`)}
                className="cursor-pointer"
              >
                <Card variant="premium">
                  <div className="p-6 text-center bg-gradient-to-br from-neon-purple/10 to-neon-pink/10">
                    <div className="flex justify-between items-center mb-4">
                      <span className="text-neon-cyan font-black">YOU</span>
                      <span className="text-neon-blue font-black text-sm animate-pulse-urgent">Scheduled</span>
                      <span className="text-neon-pink font-black">{opponent}</span>
                    </div>
                    <Button variant="primary" size="md" className="w-full font-black mt-2">ENTER MATCH</Button>
                  </div>
                </Card>
              </motion.div>
            )
          })}
        </div>
      </motion.div>
    </motion.div>
  )
}
