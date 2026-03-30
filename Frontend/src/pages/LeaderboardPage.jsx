import { useState } from 'react'
import { motion } from 'framer-motion'
import Card from '../components/Card'
import Badge from '../components/Badge'

export default function LeaderboardPage() {
  const [leaderboard] = useState([
    { rank: 1, name: 'ProGamer', points: 15000, wins: 48, level: 25, rewards: '💎👑' },
    { rank: 2, name: 'NovaStorm', points: 14500, wins: 45, level: 24, rewards: '💎' },
    { rank: 3, name: 'SkyKing', points: 14000, wins: 42, level: 23, rewards: '💎' },
    { rank: 4, name: 'LunaAce', points: 13500, wins: 39, level: 22, rewards: '' },
    { rank: 5, name: 'VortexX', points: 13000, wins: 36, level: 21, rewards: '' },
    { rank: 6, name: 'PhantomX', points: 12500, wins: 33, level: 20, rewards: '' },
    { rank: 7, name: 'TitanForce', points: 12000, wins: 30, level: 19, rewards: '' },
    { rank: 8, name: 'SilentKnight', points: 11500, wins: 27, level: 18, rewards: '' },
    { rank: 9, name: 'NetherGod', points: 11000, wins: 24, level: 17, rewards: '' },
    { rank: 10, name: 'EchoStrike', points: 10500, wins: 21, level: 16, rewards: '' },
  ])

  const getRankColor = (rank) => {
    if (rank === 1) return 'from-yellow-600 to-yellow-500'
    if (rank === 2) return 'from-gray-600 to-gray-400'
    if (rank === 3) return 'from-orange-600 to-orange-500'
    return 'from-neon-blue to-neon-purple'
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">📊 Leaderboard</h1>
        <p className="text-gray-400">Top players this season</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Top 3 Podium */}
        <div className="lg:col-span-3">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {leaderboard.slice(0, 3).map((player, idx) => (
              <motion.div
                key={player.rank}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
              >
                <Card variant="glow" hover>
                  <div className={`p-6 text-center bg-gradient-to-b ${getRankColor(player.rank)}/20`}>
                    {/* Rank Badge */}
                    <div className={`w-16 h-16 rounded-full mx-auto mb-4 flex items-center justify-center text-xl font-bold bg-gradient-to-r to-${getRankColor(player.rank).split(' ')[1]}`}>
                      {player.rank === 1 && '🥇'}
                      {player.rank === 2 && '🥈'}
                      {player.rank === 3 && '🥉'}
                    </div>

                    {/* Player Name */}
                    <h3 className="text-xl font-bold text-white mb-1">{player.name}</h3>

                    {/* Stats */}
                    <div className="space-y-2 my-4 text-sm">
                      <div>
                        <p className="text-gray-400">Points</p>
                        <p className="text-2xl font-bold text-neon-blue">{player.points.toLocaleString()}</p>
                      </div>
                      <div className="flex justify-around text-gray-400 py-2">
                        <div>
                          <p className="text-xs">Wins</p>
                          <p className="font-bold text-white">{player.wins}</p>
                        </div>
                        <div>
                          <p className="text-xs">Level</p>
                          <p className="font-bold text-white">Lv.{player.level}</p>
                        </div>
                      </div>
                    </div>

                    {/* Rewards */}
                    {player.rewards && (
                      <div className="text-2xl">{player.rewards}</div>
                    )}
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Full Leaderboard Table */}
        <div className="lg:col-span-3">
          <Card variant="elevated">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-dark-700">
                    <th className="px-6 py-4 text-left text-gray-400 font-semibold">#</th>
                    <th className="px-6 py-4 text-left text-gray-400 font-semibold">Player</th>
                    <th className="px-6 py-4 text-left text-gray-400 font-semibold">Points</th>
                    <th className="px-6 py-4 text-left text-gray-400 font-semibold">Wins</th>
                    <th className="px-6 py-4 text-left text-gray-400 font-semibold">Level</th>
                    <th className="px-6 py-4 text-left text-gray-400 font-semibold">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboard.map((player, idx) => (
                    <motion.tr
                      key={player.rank}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: idx * 0.05 }}
                      className={`border-b border-dark-700/50 hover:bg-dark-800/50 transition-smooth ${
                        idx < 3 ? 'bg-dark-800/30' : ''
                      }`}
                    >
                      <td className="px-6 py-4">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold text-white bg-gradient-to-r ${getRankColor(player.rank)}`}>
                          {player.rank}
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <p className="font-semibold text-white">{player.name}</p>
                      </td>
                      <td className="px-6 py-4">
                        <p className="font-bold text-neon-blue">{player.points.toLocaleString()}</p>
                      </td>
                      <td className="px-6 py-4">
                        <p className="text-white">{player.wins}</p>
                      </td>
                      <td className="px-6 py-4">
                        <Badge variant="primary">Lv. {player.level}</Badge>
                      </td>
                      <td className="px-6 py-4">
                        {player.rank <= 3 && <Badge variant="success">🔥 Top 3</Badge>}
                        {player.rank > 3 && player.rank <= 10 && <Badge variant="primary">Active</Badge>}
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      </div>
    </motion.div>
  )
}
