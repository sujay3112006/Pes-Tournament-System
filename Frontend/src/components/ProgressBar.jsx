import { motion } from 'framer-motion'

export default function ProgressBar({ value = 0, max = 100, label = '', variant = 'default', showGlow = true }) {
  const percentage = (value / max) * 100
  
  const variants = {
    default: 'bg-gradient-to-r from-neon-blue via-cyan-400 to-neon-purple',
    success: 'bg-gradient-to-r from-emerald-500 to-emerald-400',
    warning: 'bg-gradient-to-r from-yellow-500 to-orange-400',
    danger: 'bg-gradient-to-r from-neon-pink to-red-500',
  }

  const glowVariants = {
    default: 'shadow-glow',
    success: 'shadow-emerald-500/50',
    warning: 'shadow-yellow-500/50',
    danger: 'shadow-pink-500/50',
  }

  return (
    <div className="w-full">
      {label && (
        <div className="flex justify-between items-center mb-2">
          <p className="text-sm font-semibold text-gray-300 drop-shadow-lg">{label}</p>
          <motion.p 
            className="text-sm text-neon-blue font-bold"
            key={Math.round(percentage)}
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 0.3 }}
          >
            {Math.round(percentage)}%
          </motion.p>
        </div>
      )}
      <div className="w-full h-4 bg-dark-900/50 rounded-full overflow-hidden border border-neon-blue/20 backdrop-blur-sm">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
          className={`h-full ${variants[variant]} ${showGlow ? glowVariants[variant] : ''} relative`}
        >
          {/* Shimmer effect */}
          <motion.div
            className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent"
            animate={{ x: ['-100%', '100%'] }}
            transition={{ duration: 2, repeat: Infinity, repeatDelay: 0.5 }}
          />
        </motion.div>
      </div>
    </div>
  )
}
