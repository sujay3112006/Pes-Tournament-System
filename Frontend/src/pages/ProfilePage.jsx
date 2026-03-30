import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Card from '../components/Card'
import Badge from '../components/Badge'

export default function ProfilePage() {
  const { id } = useParams()
  const navigate = useNavigate()

  const [userProfile] = useState({
    id,
    username: 'ProGamer',
    level: 25,
    rating: 2450,
    rank: '#247',
    joinDate: '2023-06-15',
    bio: 'Competitive esports player | Trophy hunter',
    avatar: 'P',
    stats: {
      totalMatches: 456,
      wins: 320,
      losses: 136,
      winRate: 70.2,
      totalCoins: 125000,
      achievements: 24,
    },
  })

  const [matchHistory] = useState([
    { id: 1, opponent: 'NovaStorm', result: 'Win', score: '3-1', date: '10 mins ago', tournament: 'Pro Series' },
    { id: 2, opponent: 'SkyKing', result: 'Loss', score: '1-2', date: '2 hours ago', tournament: 'Ultimate Cup' },
    { id: 3, opponent: 'LunaAce', result: 'Win', score: '4-0', date: '1 day ago', tournament: 'Regional' },
    { id: 4, opponent: 'VortexX', result: 'Win', score: '2-1', date: '2 days ago', tournament: 'Spring Cup' },
    { id: 5, opponent: 'PhantomX', result: 'Win', score: '3-2', date: '3 days ago', tournament: 'Pro Series' },
  ])

  const [achievements] = useState([
    { id: 1, name: 'First Victory', icon: '🏆', date: '2023-06-16' },
    { id: 2, name: '100 Matches', icon: '🎮', date: '2023-11-20' },
    { id: 3, name: 'Win Streak x5', icon: '🔥', date: '2024-01-10' },
    { id: 4, name: 'Champion', icon: '👑', date: '2024-02-14' },
  ])

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      {/* Header */}
      <Button variant="ghost" size="sm" onClick={() => navigate(-1)} className="mb-4">
        ← Back
      </Button>

      {/* Profile Header */}
      <Card variant="glow" className="mb-8">
        <div className="p-8 bg-gradient-to-r from-neon-blue/10 to-neon-purple/10">
          <div className="flex justify-between items-start mb-6">
            <div className="flex items-center gap-6">
              <div className="w-24 h-24 rounded-full bg-gradient-to-r from-neon-blue to-neon-purple flex items-center justify-center text-4xl font-bold">
                {userProfile.avatar}
              </div>
              <div>
                <h1 className="text-4xl font-bold text-white mb-1">{userProfile.username}</h1>
                <p className="text-gray-400 mb-4">{userProfile.bio}</p>
                <div className="flex gap-3">
                  <Badge variant="primary">Rank {userProfile.rank}</Badge>
                  <Badge variant="purple">Level {userProfile.level}</Badge>
                </div>
              </div>
            </div>
            <Button variant="primary" size="lg">Follow</Button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mt-8 pt-8 border-t border-white/10">
            {[
              { label: 'Matches', value: userProfile.stats.totalMatches },
              { label: 'Win Rate', value: `${userProfile.stats.winRate}%` },
              { label: 'Rank Rating', value: userProfile.rating },
              { label: 'Coins', value: `${(userProfile.stats.totalCoins / 1000).toFixed(0)}k` },
              { label: 'Achievements', value: userProfile.stats.achievements },
            ].map((stat, idx) => (
              <div key={idx} className="text-center">
                <p className="text-gray-400 text-sm mb-1">{stat.label}</p>
                <p className="text-2xl font-bold text-neon-blue">{stat.value}</p>
              </div>
            ))}
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Match History */}
          <Card variant="elevated">
            <div className="p-6">
              <h2 className="text-2xl font-bold text-white mb-6">📜 Recent Matches</h2>
              <div className="space-y-3">
                {matchHistory.map((match, idx) => (
                  <motion.div
                    key={match.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    className="flex items-center justify-between p-4 bg-dark-800/50 rounded-lg hover:bg-dark-700 transition-smooth"
                  >
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-1">
                        <span className="font-semibold text-white">vs {match.opponent}</span>
                        <Badge variant={match.result === 'Win' ? 'success' : 'danger'} size="sm">
                          {match.result}
                        </Badge>
                      </div>
                      <div className="flex gap-4 text-sm">
                        <span className="text-gray-400">{match.tournament}</span>
                        <span className="text-gray-500">{match.date}</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-lg font-bold text-neon-blue">{match.score}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Achievements */}
          <Card variant="glow">
            <div className="p-6">
              <h3 className="text-xl font-bold text-white mb-4">🎖️ Achievements</h3>
              <div className="grid grid-cols-2 gap-3">
                {achievements.map((achievement, idx) => (
                  <motion.div
                    key={achievement.id}
                    whileHover={{ scale: 1.05 }}
                    className="p-3 bg-dark-800 rounded-lg text-center hover:bg-dark-700 transition-smooth cursor-pointer"
                    title={`${achievement.name} - ${achievement.date}`}
                  >
                    <div className="text-2xl mb-1">{achievement.icon}</div>
                    <p className="text-xs text-gray-300">{achievement.name.split(' ')[0]}</p>
                  </motion.div>
                ))}
              </div>
            </div>
          </Card>

          {/* Info */}
          <Card variant="dark">
            <div className="p-6 space-y-4 text-sm">
              <div>
                <p className="text-gray-400 mb-1">Member Since</p>
                <p className="font-semibold text-white">{userProfile.joinDate}</p>
              </div>
              <div>
                <p className="text-gray-400 mb-1">Total Wins</p>
                <p className="font-semibold text-green-400">{userProfile.stats.wins}</p>
              </div>
              <div>
                <p className="text-gray-400 mb-1">Total Losses</p>
                <p className="font-semibold text-red-400">{userProfile.stats.losses}</p>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </motion.div>
  )
}
