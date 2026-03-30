import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Card from '../components/Card'
import Badge from '../components/Badge'
import ProgressBar from '../components/ProgressBar'

export default function TournamentDetailsPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [tournament] = useState({
    id,
    name: 'Spring Championship 2026',
    format: 'Knockout',
    description: 'Compete with the best players and win amazing prizes!',
    players: 18,
    maxPlayers: 64,
    status: 'upcoming',
    prize: '$10,000',
    entryFee: '$50',
    startDate: '2026-04-01',
    registered: true,
  })

  const [players] = useState([
    { id: 1, name: 'ProGamer', rank: 1, rating: 92 },
    { id: 2, name: 'NovaStorm', rank: 2, rating: 89 },
    { id: 3, name: 'SkyKing', rank: 3, rating: 88 },
    { id: 4, name: 'LunaAce', rank: 4, rating: 87 },
  ])

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      {/* Header */}
      <div className="mb-8">
        <Button variant="ghost" size="sm" onClick={() => navigate(-1)} className="mb-4">
          ← Back
        </Button>
        <h1 className="text-4xl font-bold text-white mb-2">{tournament.name}</h1>
        <p className="text-gray-400">{tournament.description}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Tournament Info */}
          <Card variant="glow">
            <div className="p-6">
              <h2 className="text-2xl font-bold text-white mb-4">Tournament Details</h2>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-gray-400 text-sm mb-1">Format</p>
                  <p className="text-lg font-semibold text-neon-blue">{tournament.format}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-sm mb-1">Status</p>
                  <Badge variant={tournament.status === 'ongoing' ? 'success' : 'primary'}>
                    {tournament.status}
                  </Badge>
                </div>
                <div>
                  <p className="text-gray-400 text-sm mb-1">Prize Pool</p>
                  <p className="text-lg font-semibold text-neon-pink">💰 {tournament.prize}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-sm mb-1">Entry Fee</p>
                  <p className="text-lg font-semibold text-white">{tournament.entryFee}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-sm mb-1">Start Date</p>
                  <p className="text-lg font-semibold text-white">{tournament.startDate}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-sm mb-1">Max Players</p>
                  <p className="text-lg font-semibold text-white">{tournament.maxPlayers}</p>
                </div>
              </div>
            </div>
          </Card>

          {/* Players Section */}
          <Card variant="glow">
            <div className="p-6">
              <h2 className="text-2xl font-bold text-white mb-4">
                Registered Players ({tournament.players}/{tournament.maxPlayers})
              </h2>
              <ProgressBar
                value={tournament.players}
                max={tournament.maxPlayers}
                label="Registration Progress"
              />
              <div className="mt-6 space-y-2">
                {players.map((player, idx) => (
                  <motion.div
                    key={player.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    className="flex items-center justify-between p-3 bg-dark-800 rounded-lg hover:bg-dark-700 transition-smooth"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-gradient-to-r from-neon-blue to-neon-purple flex items-center justify-center text-sm font-bold">
                        {player.rank}
                      </div>
                      <div>
                        <p className="font-semibold text-white">{player.name}</p>
                        <p className="text-xs text-gray-400">Rating: {player.rating}</p>
                      </div>
                    </div>
                    <Badge variant="primary" size="sm">
                      Rank #{player.rank}
                    </Badge>
                  </motion.div>
                ))}
              </div>
            </div>
          </Card>
        </div>

        {/* Sidebar */}
        <div>
          <Card variant="glow">
            <div className="p-6 space-y-4">
              <div>
                <p className="text-gray-400 text-sm mb-2">Your Status</p>
                <Badge variant={tournament.registered ? 'success' : 'warning'}>
                  {tournament.registered ? '✓ Registered' : 'Not Registered'}
                </Badge>
              </div>

              {!tournament.registered ? (
                <Button variant="primary" size="lg" className="w-full">
                  Join Tournament
                </Button>
              ) : (
                <>
                  <Button variant="primary" size="lg" className="w-full">
                    View Bracket
                  </Button>
                  <Button
                    variant="danger"
                    size="lg"
                    className="w-full"
                  >
                    Leave Tournament
                  </Button>
                </>
              )}

              {/* Quick Stats */}
              <div className="pt-4 border-t border-dark-700 space-y-3">
                <h3 className="font-semibold text-white">Quick Stats</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Spots Left</span>
                    <span className="font-semibold text-neon-blue">
                      {tournament.maxPlayers - tournament.players}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Registration Fee</span>
                    <span className="font-semibold text-neon-pink">
                      {tournament.entryFee}
                    </span>
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
