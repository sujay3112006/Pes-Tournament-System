import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Card from '../components/Card'
import Tabs from '../components/Tabs'
import TournamentCard from '../components/TournamentCard'
import Loader from '../components/Loader'

export default function TournamentListPage() {
  const navigate = useNavigate()
  const [activeFilter, setActiveFilter] = useState('upcoming')
  const [loading, setLoading] = useState(false)

  const tabs = [
    { id: 'ongoing', label: 'Ongoing' },
    { id: 'upcoming', label: 'Upcoming' },
    { id: 'completed', label: 'Completed' },
  ]

  const tournaments = {
    ongoing: [
      { id: 1, name: 'Ultimate Cup 2026', format: 'Knockout', players: 32, maxPlayers: 32, status: 'ongoing', prize: '$5,000' },
      { id: 2, name: 'Pro Series', format: 'League', players: 28, maxPlayers: 32, status: 'ongoing', prize: '$3,000' },
    ],
    upcoming: [
      { id: 3, name: 'Spring Championship', format: 'Knockout', players: 18, maxPlayers: 64, status: 'upcoming', prize: '$10,000' },
      { id: 4, name: 'Regional Qualifier', format: 'League', players: 12, maxPlayers: 32, status: 'upcoming', prize: '$2,000' },
      { id: 5, name: 'Esports Masters', format: 'Knockout', players: 8, maxPlayers: 16, status: 'upcoming', prize: '$15,000' },
    ],
    completed: [
      { id: 6, name: 'Winter Championship 2025', format: 'Knockout', players: 32, maxPlayers: 32, status: 'completed', prize: '$8,000' },
      { id: 7, name: 'Fall Series 2025', format: 'League', players: 32, maxPlayers: 32, status: 'completed', prize: '$5,000' },
    ],
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      {/* Header */}
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">🏆 Tournaments</h1>
          <p className="text-gray-400">Browse and join exciting tournaments</p>
        </div>
        <Button
          variant="primary"
          size="lg"
          onClick={() => navigate('/tournaments/create')}
        >
          Create Tournament
        </Button>
      </div>

      {/* Tabs */}
      <Tabs
        tabs={tabs}
        activeTab={activeFilter}
        onTabChange={setActiveFilter}
      />

      {/* Loading State */}
      {loading && (
        <div className="flex justify-center py-12">
          <Loader message="Loading tournaments..." />
        </div>
      )}

      {/* Tournament Grid */}
      {!loading && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tournaments[activeFilter].map((tournament, idx) => (
            <motion.div
              key={tournament.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
              onClick={() => navigate(`/tournaments/${tournament.id}`)}
            >
              <TournamentCard
                name={tournament.name}
                format={tournament.format}
                players={tournament.players}
                maxPlayers={tournament.maxPlayers}
                status={tournament.status}
                prize={tournament.prize}
              />
            </motion.div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && tournaments[activeFilter].length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-400 text-lg mb-4">No tournaments found</p>
          <Button
            variant="primary"
            onClick={() => navigate('/tournaments/create')}
          >
            Create the first one
          </Button>
        </div>
      )}
    </motion.div>
  )
}
