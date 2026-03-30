import { motion } from 'framer-motion'

export default function PlayerCard({
  image = '/placeholder.jpg',
  name = 'Player Name',
  position = 'ST',
  rating = 88,
  price = '$5000',
  onClick = () => {},
  team = 'Team',
  country = '🌍',
}) {
  return (
    <motion.div
      whileHover={{ y: -12, rotateZ: 2 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      className="cursor-pointer"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <div className="relative w-full aspect-[3/4] rounded-2xl overflow-hidden group">
        {/* Main gradient border */}
        <div className="absolute inset-0 bg-gradient-to-br from-neon-blue via-neon-purple to-neon-pink rounded-2xl p-1 opacity-80 group-hover:opacity-100 transition-opacity duration-300">
          <div className="absolute inset-1 bg-dark-900/90 rounded-xl" />
        </div>

        {/* Card content */}
        <div className="relative inset-0 bg-gradient-to-b from-dark-800/80 to-dark-950 flex items-center justify-center overflow-hidden">
          {/* Shine effect background */}
          <motion.div
            className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent"
            animate={{
              x: ['100%', '-100%'],
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              repeatDelay: 2,
            }}
            style={{ pointerEvents: 'none' }}
          />

          {/* Image */}
          <img
            src={image}
            alt={name}
            className="w-full h-full object-cover group-hover:scale-125 transition-transform duration-500 filter brightness-110"
          />

          {/* Overlay gradient */}
          <div className="absolute inset-0 bg-gradient-to-t from-dark-950 via-transparent to-transparent" />
        </div>

        {/* Rating Badge - PES Style */}
        <motion.div
          whileHover={{ scale: 1.15, rotate: 5 }}
          className="absolute top-4 right-4 bg-gradient-to-br from-yellow-400 to-orange-500 text-dark-900 font-black rounded-xl w-16 h-16 flex items-center justify-center text-2xl shadow-lg ring-2 ring-yellow-300/50 z-20"
        >
          {rating}
        </motion.div>

        {/* Position Badge */}
        <motion.div
          whileHover={{ scale: 1.1 }}
          className="absolute top-4 left-4 bg-gradient-to-r from-neon-blue to-cyan-400 text-dark-900 font-black px-3 py-1.5 rounded-lg text-sm shadow-lg ring-1 ring-neon-blue/50 z-20"
        >
          {position}
        </motion.div>

        {/* Country Flag */}
        <div className="absolute top-4 left-24 text-2xl">{country}</div>

        {/* Info Section */}
        <div className="absolute bottom-0 left-0 right-0 p-4 z-10 bg-gradient-to-t from-dark-950 via-dark-950/80 to-transparent">
          <h3 className="text-lg font-black text-white mb-1 truncate drop-shadow-lg">{name}</h3>
          <p className="text-xs text-gray-400 mb-2 truncate">{team}</p>
          <p className="text-neon-blue font-black text-lg drop-shadow-lg">{price}</p>
        </div>

        {/* Glow effect on hover */}
        <motion.div
          className="absolute inset-0 rounded-2xl pointer-events-none"
          initial={{ boxShadow: '0 0 0 rgba(0, 240, 255, 0)' }}
          whileHover={{ 
            boxShadow: '0 0 30px rgba(0, 240, 255, 0.5), inset 0 0 30px rgba(0, 240, 255, 0.1)'
          }}
          transition={{ duration: 0.3 }}
        />
      </div>
    </motion.div>
  )
}
