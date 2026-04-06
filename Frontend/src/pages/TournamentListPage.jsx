import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import Button from '../components/Button'
import Tabs from '../components/Tabs'
import TournamentCard from '../components/TournamentCard'
import Loader from '../components/Loader'
import { tournamentService } from '../services/api'

const STATUS_MAP = {
  registration: 'registration',
  active: 'active',
  completed: 'completed',
}

export default function TournamentListPage() {
  const navigate = useNavigate()
  const [activeFilter, setActiveFilter] = useState('registration')
  const [tournaments, setTournaments] = useState([])
  const [loading, setLoading] = useState(false)

  const tabs = [
    { id: 'registration', label: 'Open' },
    { id: 'active', label: 'Ongoing' },
    { id: 'completed', label: 'Completed' },
  ]

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      try {
        const { data } = await tournamentService.getAll({ status: STATUS_MAP[activeFilter] })
        const tournaments = data.tournaments || data.results || (Array.isArray(data) ? data : [])
        setTournaments(tournaments)
      } catch (err) {
        console.error('Failed to load tournaments:', err)
        setTournaments([])
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [activeFilter])

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">🏆 Tournaments</h1>
          <p className="text-gray-400">Browse and join exciting tournaments</p>
        </div>
        <Button variant="primary" size="lg" onClick={() => navigate('/tournaments/create')}>
          Create Tournament
        </Button>
      </div>

      <Tabs tabs={tabs} activeTab={activeFilter} onTabChange={setActiveFilter} />

      {loading && (
        <div className="flex justify-center py-12">
          <Loader message="Loading tournaments..." />
        </div>
      )}

      {!loading && tournaments.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tournaments.map((t, idx) => (
            <motion.div
              key={t.tournament_id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
              onClick={() => navigate(`/tournaments/${t.tournament_id}`)}
            >
              <TournamentCard
                name={t.name}
                format={t.format}
                players={t.current_players}
                maxPlayers={t.max_players}
                status={t.status}
                prize={`${t.prize_pool?.toLocaleString() ?? 0} coins`}
              />
            </motion.div>
          ))}
        </div>
      )}

      {!loading && tournaments.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-400 text-lg mb-4">No tournaments found</p>
          <Button variant="primary" onClick={() => navigate('/tournaments/create')}>
            Create the first one
          </Button>
        </div>
      )}
    </motion.div>
  )
}
