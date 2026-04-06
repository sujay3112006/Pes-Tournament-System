import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import Card from '../components/Card'
import Badge from '../components/Badge'
import Loader from '../components/Loader'
import { leaderboardService } from '../services/api'

export default function LeaderboardPage({ user }) {
  const [entries, setEntries] = useState([])
  const [topPlayers, setTopPlayers] = useState([])
  const [myRank, setMyRank] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        const [topRes, rankRes] = await Promise.all([
          leaderboardService.getTopPlayers({ limit: 10 }),
          leaderboardService.getRankings({ limit: 20 }),
        ])
        const topPlayers = topRes.data.results || topRes.data.top_players || (Array.isArray(topRes.data) ? topRes.data : [])
        const rankings = rankRes.data.results || rankRes.data.rankings || (Array.isArray(rankRes.data) ? rankRes.data : [])
        setTopPlayers(topPlayers)
        setEntries(rankings)
      } catch (err) {
        console.error('Leaderboard load error:', err)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const getRankColor = (rank) => {
    if (rank === 1) return 'from-yellow-600 to-yellow-500'
    if (rank === 2) return 'from-gray-600 to-gray-400'
    if (rank === 3) return 'from-orange-600 to-orange-500'
    return 'from-neon-blue to-neon-purple'
  }

  if (loading) return <div className="flex justify-center py-20"><Loader message="Loading leaderboard..." /></div>

  const displayList = entries.length > 0 ? entries : topPlayers

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">📊 Leaderboard</h1>
        <p className="text-gray-400">Top players this season</p>
      </div>

      {/* Top 3 Podium */}
      {topPlayers.length >= 3 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {topPlayers.slice(0, 3).map((player, idx) => (
            <motion.div key={player.user_id || idx} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: idx * 0.1 }}>
              <Card variant="glow" hover>
                <div className={`p-6 text-center`}>
                  <div className="w-16 h-16 rounded-full mx-auto mb-4 flex items-center justify-center text-3xl">
                    {idx === 0 && '🥇'}{idx === 1 && '🥈'}{idx === 2 && '🥉'}
                  </div>
                  <h3 className="text-xl font-bold text-white mb-1">{player.username}</h3>
                  <div className="space-y-2 my-4 text-sm">
                    <p className="text-2xl font-bold text-neon-blue">{player.points?.toLocaleString() ?? 0} pts</p>
                    <div className="flex justify-around text-gray-400 py-2">
                      <div><p className="text-xs">Wins</p><p className="font-bold text-white">{player.wins ?? 0}</p></div>
                      <div><p className="text-xs">Win Rate</p><p className="font-bold text-white">{player.win_rate?.toFixed(1) ?? 0}%</p></div>
                    </div>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      )}

      {/* Full Table */}
      <Card variant="elevated">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-dark-700">
                <th className="px-6 py-4 text-left text-gray-400 font-semibold">#</th>
                <th className="px-6 py-4 text-left text-gray-400 font-semibold">Player</th>
                <th className="px-6 py-4 text-left text-gray-400 font-semibold">Points</th>
                <th className="px-6 py-4 text-left text-gray-400 font-semibold">Wins</th>
                <th className="px-6 py-4 text-left text-gray-400 font-semibold">Win Rate</th>
                <th className="px-6 py-4 text-left text-gray-400 font-semibold">Status</th>
              </tr>
            </thead>
            <tbody>
              {displayList.map((player, idx) => {
                const rank = player.rank ?? player.position ?? idx + 1
                const isMe = player.user_id === user?.user_id
                return (
                  <motion.tr
                    key={player.user_id || idx}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: idx * 0.04 }}
                    className={`border-b border-dark-700/50 hover:bg-dark-800/50 transition-smooth ${isMe ? 'bg-neon-blue/10' : ''}`}
                  >
                    <td className="px-6 py-4">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold text-white bg-gradient-to-r ${getRankColor(rank)}`}>
                        {rank}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <p className="font-semibold text-white">{player.username}{isMe && ' (You)'}</p>
                    </td>
                    <td className="px-6 py-4">
                      <p className="font-bold text-neon-blue">{player.points?.toLocaleString() ?? 0}</p>
                    </td>
                    <td className="px-6 py-4"><p className="text-white">{player.wins ?? 0}</p></td>
                    <td className="px-6 py-4"><p className="text-white">{player.win_rate?.toFixed(1) ?? 0}%</p></td>
                    <td className="px-6 py-4">
                      {rank <= 3 && <Badge variant="success">🔥 Top 3</Badge>}
                      {rank > 3 && rank <= 10 && <Badge variant="primary">Active</Badge>}
                    </td>
                  </motion.tr>
                )
              })}
            </tbody>
          </table>
          {displayList.length === 0 && (
            <p className="text-gray-400 text-center py-12">No leaderboard data yet.</p>
          )}
        </div>
      </Card>
    </motion.div>
  )
}
