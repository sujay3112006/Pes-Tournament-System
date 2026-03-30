import { motion } from 'framer-motion'
import Card from './Card'

export default function TournamentCard({
  name = 'Tournament Name',
  format = 'Knockout',
  players = 0,
  maxPlayers = 32,
  status = 'upcoming',
  prize = '$10,000',
  onClick = () => {},
}) {
  const statusColors = {
    ongoing: 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/50 shadow-emerald-500/50',
    upcoming: 'bg-neon-blue/20 text-neon-blue border border-neon-blue/50 shadow-glow',
    completed: 'bg-gray-500/20 text-gray-400 border border-gray-500/50',
  }

  const statusPulse = status === 'ongoing' ? 'pulse-urgent' : ''

  return (
    <motion.div 
      whileHover={{ y: -12 }} 
      onClick={onClick} 
      className="cursor-pointer"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <Card variant="glow" animate={true}>
        <div className="p-6">
          {/* Header */}
          <div className="flex justify-between items-start mb-4">
            <div className="flex-1">
              <h3 className="text-lg font-bold text-white mb-1 drop-shadow-lg">{name}</h3>
              <p className="text-gray-400 text-sm">{format} Format</p>
            </div>
            <motion.span 
              className={`px-3 py-1.5 rounded-full text-xs font-bold ${statusColors[status]} ${statusPulse}`}
              animate={status === 'ongoing' ? { scale: [1, 1.05, 1] } : {}}
              transition={{ duration: 2, repeat: Infinity }}
            >
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </motion.span>
          </div>

          {/* Players Progress */}
          <div className="mb-5">
            <div className="flex justify-between mb-2">
              <span className="text-sm text-gray-400 font-semibold">Players</span>
              <motion.span 
                className="text-sm font-bold text-neon-blue drop-shadow-lg"
                key={players}
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 0.3 }}
              >
                {players}/{maxPlayers}
              </motion.span>
            </div>
            <div className="w-full h-3 bg-dark-900/50 rounded-full overflow-hidden border border-neon-blue/20">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${(players / maxPlayers) * 100}%` }}
                transition={{ duration: 0.6, ease: 'easeOut' }}
                className="h-full bg-gradient-to-r from-neon-blue via-cyan-400 to-neon-purple shadow-glow relative"
              >
                <motion.div
                  className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent"
                  animate={{ x: ['-100%', '100%'] }}
                  transition={{ duration: 2, repeat: Infinity, repeatDelay: 0.5 }}
                />
              </motion.div>
            </div>
          </div>

          {/* Prize */}
          <motion.div 
            className="flex items-center text-neon-cyan font-bold drop-shadow-lg"
            whileHover={{ scale: 1.05 }}
          >
            <span className="mr-2 text-lg">💰</span>
            {prize}
          </motion.div>
        </div>
      </Card>
    </motion.div>
  )
}
