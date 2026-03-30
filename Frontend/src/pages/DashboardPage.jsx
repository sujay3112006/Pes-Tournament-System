import { motion } from 'framer-motion'
import { useState } from 'react'
import Button from '../components/Button'
import Card from '../components/Card'
import Badge from '../components/Badge'
import { useNavigate } from 'react-router-dom'

export default function DashboardPage() {
  const navigate = useNavigate()
  const [userStats] = useState({
    username: 'ProGamer',
    level: 15,
    coins: 15000,
    wins: 48,
    losses: 12,
    rank: 247,
  })

  const activeTournaments = [
    { id: 1, name: 'Ultimate Cup 2026', players: 28, maxPlayers: 32, prize: '$5,000', status: 'ongoing' },
    { id: 2, name: 'Spring Championship', players: 45, maxPlayers: 64, prize: '$10,000', status: 'upcoming' },
  ]

  const upcomingMatches = [
    { id: 1, opponent: 'SkyKing', time: '2 hours', prize: '$500' },
    { id: 2, opponent: 'NovaStorm', time: '5 hours', prize: '$300' },
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0.2 }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } }
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
      {/* Hero Header */}
      <motion.div className="mb-10" initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <motion.h1 
          className="text-5xl font-black bg-gradient-to-r from-neon-blue via-neon-cyan to-neon-purple bg-clip-text text-transparent mb-3 drop-shadow-xl"
          animate={{ scale: [0.98, 1, 0.98] }}
          transition={{ duration: 3, repeat: Infinity }}
        >
          Welcome back, <span className="text-neon-cyan">{userStats.username}</span>!
        </motion.h1>
        <motion.p 
          className="text-gray-300 font-semibold text-lg"
          animate={{ opacity: [0.7, 1, 0.7] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          🎮 Ready to dominate? Your tournament awaits...
        </motion.p>
      </motion.div>

      {/* Stats Grid - Gaming Style */}
      <motion.div 
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-10"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {[
          { label: 'LEVEL', value: userStats.level, icon: '⭐', color: 'from-yellow-400 to-orange-400' },
          { label: 'COINS', value: `${userStats.coins.toLocaleString()}`, icon: '💰', color: 'from-emerald-400 to-green-400' },
          { label: 'WINS', value: userStats.wins, icon: '🏆', color: 'from-neon-cyan to-neon-blue' },
          { label: 'RANK', value: `#${userStats.rank}`, icon: '📊', color: 'from-neon-pink to-red-400' },
        ].map((stat, idx) => (
          <motion.div
            key={idx}
            variants={itemVariants}
          >
            <motion.div
              whileHover={{ y: -12, scale: 1.02 }}
              className="h-full"
            >
              <Card variant="premium" className="h-full">
                <div className={`p-6 text-center bg-gradient-to-br ${stat.color} bg-opacity-5`}>
                  <motion.div 
                    className="text-5xl mb-3"
                    animate={{ scale: [1, 1.1, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    {stat.icon}
                  </motion.div>
                  <p className="text-gray-400 text-xs font-black uppercase tracking-widest mb-2">{stat.label}</p>
                  <motion.p 
                    className={`text-3xl font-black bg-gradient-to-r ${stat.color} bg-clip-text text-transparent`}
                    animate={{ scale: [1, 1.05, 1] }}
                    transition={{ duration: 2, repeat: Infinity, delay: 0.2 }}
                  >
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
        <motion.div 
          className="lg:col-span-2"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
        >
          <h2 className="text-3xl font-black text-white mb-5 flex items-center gap-3 drop-shadow-lg">
            🏆 ACTIVE TOURNAMENTS
            <span className="animate-pulse-urgent inline-block w-3 h-3 bg-neon-cyan rounded-full"></span>
          </h2>
          <div className="space-y-4">
            {activeTournaments.map((tournament, idx) => (
              <motion.div
                key={tournament.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + idx * 0.1 }}
                onClick={() => navigate(`/tournaments/${tournament.id}`)}
                className="cursor-pointer"
              >
                <Card variant="glow" hover>
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-5">
                      <div className="flex-1">
                        <h3 className="text-xl font-black text-white drop-shadow-lg">{tournament.name}</h3>
                        <Badge 
                          variant="primary" 
                          size="md" 
                          className="mt-3 font-bold"
                        >
                          {tournament.players}/{tournament.maxPlayers} Players
                        </Badge>
                      </div>
                      <motion.div
                        animate={tournament.status === 'ongoing' ? { scale: [1, 1.05, 1] } : {}}
                        transition={{ duration: 1, repeat: Infinity }}
                      >
                        <Badge 
                          variant={tournament.status === 'ongoing' ? 'success' : 'primary'}
                          size="md"
                          className="font-black"
                        >
                          {tournament.status.toUpperCase()}
                        </Badge>
                      </motion.div>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-neon-cyan font-black text-lg drop-shadow-lg">💰 {tournament.prize}</span>
                      <Button variant="secondary" size="md" className="font-bold">
                        VIEW DETAILS
                      </Button>
                    </div>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Quick Actions - Gaming Menu */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
        >
          <h2 className="text-3xl font-black text-white mb-5 drop-shadow-lg">⚡ QUICK ACTIONS</h2>
          <div className="space-y-3">
            {[
              { label: 'JOIN TOURNAMENT', action: '/tournaments', icon: '🎮', color: 'primary' },
              { label: 'CREATE TOURNAMENT', action: '/tournaments/create', icon: '🏗️', color: 'accent' },
              { label: 'LIVE AUCTION', action: '/auction', icon: '💎', color: 'secondary' },
              { label: 'DAILY MISSIONS', action: '/missions', icon: '🎯', color: 'ghost' },
            ].map((action, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + idx * 0.08 }}
              >
                <Button
                  variant={action.color}
                  size="lg"
                  className="w-full justify-center font-black text-base"
                  onClick={() => navigate(action.action)}
                >
                  <span className="mr-2">{action.icon}</span>
                  {action.label}
                </Button>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Upcoming Matches - Gaming Event Style */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
      >
        <h2 className="text-3xl font-black text-white mb-5 flex items-center gap-3 drop-shadow-lg">
          ⚔️ UPCOMING BATTLES
          <span className="animate-pulse-urgent inline-block w-3 h-3 bg-neon-pink rounded-full"></span>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {upcomingMatches.map((match, idx) => (
            <motion.div
              key={match.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7 + idx * 0.1 }}
              whileHover={{ y: -8 }}
              onClick={() => navigate(`/match/${match.id}`)}
              className="cursor-pointer"
            >
              <Card variant="premium">
                <div className="p-6 text-center bg-gradient-to-br from-neon-purple/10 to-neon-pink/10">
                  <div className="flex justify-between items-center mb-4">
                    <span className="text-neon-cyan font-black">YOU</span>
                    <span className="text-neon-blue font-black text-sm animate-pulse-urgent">{match.time}</span>
                    <span className="text-neon-pink font-black">{match.opponent}</span>
                  </div>
                  <motion.h3 
                    className="text-3xl font-black text-white mb-5 drop-shadow-lg"
                    animate={{ scale: [1, 1.02, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    BATTLE READY
                  </motion.h3>
                  <div className="flex justify-between items-center gap-3">
                    <span className="text-neon-cyan font-black text-lg">💰 {match.prize}</span>
                    <Button variant="primary" size="md" className="flex-1 font-black">
                      ENTER MATCH
                    </Button>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </motion.div>
  )
}
